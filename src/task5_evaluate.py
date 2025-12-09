#!/usr/bin/env python3
"""
Task 5 Evaluation Script
Calculates metrics for neuroscience LITERATURE job performance
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import re

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

# For Kendall's tau correlation
try:
    from scipy.stats import kendalltau
except ImportError:
    print("Warning: scipy not installed, ranking correlation will be set to 0")
    kendalltau = None


def calculate_mechanism_recall(identified, ground_truth):
    """% of established mechanisms identified by Kosmos"""
    identified_lower = [m.lower() for m in identified]
    gt_mechanisms = [m["name"].lower() for m in ground_truth["established_mechanisms"]]

    overlap = 0
    matched_mechanisms = []

    for gt_mech in gt_mechanisms:
        # Check if any identified mechanism contains key terms
        key_terms = gt_mech.split()[:2]  # E.g., "alpha-synuclein propagation"

        for id_mech in identified_lower:
            if all(term in id_mech for term in key_terms):
                overlap += 1
                matched_mechanisms.append(gt_mech)
                break

    recall = overlap / len(gt_mechanisms) if gt_mechanisms else 0
    return recall, matched_mechanisms


def evaluate_intervention_ranking(kosmos_ranking, expected_order):
    """Kendall's tau for ranking quality"""
    if kendalltau is None:
        return 0, 0, "scipy not available"

    # Map intervention names to positions
    kosmos_positions = {}
    for i, item in enumerate(kosmos_ranking):
        if isinstance(item, str):
            kosmos_positions[item.lower()] = i
        elif isinstance(item, dict) and "intervention" in item:
            kosmos_positions[item["intervention"].lower()] = i

    expected_positions = {intervention.lower(): i for i, intervention in enumerate(expected_order)}

    # Get overlapping interventions
    common = set(kosmos_positions.keys()) & set(expected_positions.keys())

    if len(common) < 2:
        return 0, len(common), f"Only {len(common)} common interventions"

    kosmos_ranks = [kosmos_positions[item] for item in common]
    expected_ranks = [expected_positions[item] for item in common]

    tau, p_value = kendalltau(kosmos_ranks, expected_ranks)
    return tau, len(common), f"p={p_value:.3f}"


def count_primary_research_citations(citations):
    """% of citations that are primary research (not reviews)"""
    if not citations:
        return 0, 0, 0

    primary_count = 0
    review_count = 0
    other_count = 0

    for citation in citations:
        if isinstance(citation, str):
            citation_text = citation.lower()
        elif isinstance(citation, dict):
            citation_text = str(citation).lower()
        else:
            citation_text = str(citation).lower()

        # Heuristics to identify review vs primary research
        if any(term in citation_text for term in ["review", "perspective", "opinion", "editorial"]):
            review_count += 1
        elif any(term in citation_text for term in ["journal", "nature", "science", "cell"]):
            primary_count += 1
        else:
            other_count += 1

    total = len(citations)
    primary_ratio = primary_count / total if total > 0 else 0

    return primary_ratio, primary_count, total


def extract_key_papers_coverage(citations, ground_truth):
    """Check if key papers from ground truth are cited"""
    key_dois = [paper["doi"] if isinstance(paper, dict) else paper
                for mech in ground_truth["established_mechanisms"]
                for paper in mech.get("key_papers", [])]

    coverage = {}
    for doi in key_dois:
        # Check if DOI appears in citations
        found = False
        for citation in citations:
            if isinstance(citation, str):
                if doi in citation:
                    found = True
                    break
            elif isinstance(citation, dict):
                if "doi" in citation and citation["doi"] == doi:
                    found = True
                    break

        coverage[doi] = found

    return coverage


def main():
    """Main evaluation function"""
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / "output" / "task5_results"
    input_dir = base_dir / "input"

    # Load ground truth
    ground_truth_file = input_dir / "task5_ground_truth.json"
    with open(ground_truth_file) as f:
        ground_truth = json.load(f)

    # Load Kosmos results
    results_file = output_dir / "kosmos_raw_output.json"
    if not results_file.exists():
        print(f"Error: Results file {results_file} not found")
        sys.exit(1)

    with open(results_file) as f:
        kosmos_data = json.load(f)

    # Load parsed results if available
    parsed_file = output_dir / "parsed_results.json"
    if parsed_file.exists():
        with open(parsed_file) as f:
            parsed = json.load(f)
    else:
        parsed = {"identified_mechanisms": [], "ranked_interventions": [], "citations": []}
        # Try to extract from raw results
        if "results" in kosmos_data:
            results = kosmos_data["results"]
            if isinstance(results, dict):
                parsed["identified_mechanisms"] = results.get("mechanisms", [])
                parsed["ranked_interventions"] = results.get("interventions", [])
                parsed["citations"] = results.get("citations", [])

    # Calculate metrics
    metrics = {
        "evaluation_timestamp": datetime.now().isoformat(),
        "task_id": kosmos_data.get("task_id"),
    }

    # 1. Mechanism recall
    identified_mechanisms = parsed.get("identified_mechanisms", [])
    recall, matched = calculate_mechanism_recall(identified_mechanisms, ground_truth)
    metrics["mechanism_recall"] = {
        "value": recall,
        "percentage": recall * 100,
        "matched_mechanisms": matched,
        "total_ground_truth": len(ground_truth["established_mechanisms"]),
        "identified_count": len(identified_mechanisms)
    }

    # 2. Intervention ranking quality
    kosmos_ranking = parsed.get("ranked_interventions", [])
    expected_order = ground_truth["expected_ranking_order"]
    tau, common_count, details = evaluate_intervention_ranking(kosmos_ranking, expected_order)
    metrics["intervention_ranking"] = {
        "kendall_tau": tau,
        "common_interventions": common_count,
        "details": details,
        "kosmos_ranking": kosmos_ranking[:5] if kosmos_ranking else [],  # Top 5
        "expected_ranking": expected_order
    }

    # 3. Citation metrics
    citations = parsed.get("citations", [])
    primary_ratio, primary_count, total_count = count_primary_research_citations(citations)
    metrics["citation_metrics"] = {
        "total_citations": total_count,
        "primary_research_count": primary_count,
        "primary_research_ratio": primary_ratio,
        "primary_research_percentage": primary_ratio * 100
    }

    # 4. Key papers coverage
    if citations:
        key_coverage = extract_key_papers_coverage(citations, ground_truth)
        covered_count = sum(key_coverage.values())
        metrics["key_papers_coverage"] = {
            "coverage": key_coverage,
            "covered_count": covered_count,
            "total_key_papers": len(key_coverage),
            "coverage_percentage": (covered_count / len(key_coverage)) * 100 if key_coverage else 0
        }

    # 5. Pass/Fail determination
    targets = {
        "mechanism_recall": 0.75,  # ≥75%
        "intervention_ranking": 0.5,  # τ ≥ 0.5
        "citation_count": 15,  # ≥15 citations
        "primary_research_ratio": 0.6  # ≥60%
    }

    passes = {
        "mechanism_recall": recall >= targets["mechanism_recall"],
        "intervention_ranking": tau >= targets["intervention_ranking"],
        "citation_count": total_count >= targets["citation_count"],
        "primary_research_ratio": primary_ratio >= targets["primary_research_ratio"]
    }

    metrics["targets"] = targets
    metrics["passes"] = passes
    metrics["overall_pass"] = sum(passes.values()) >= 3  # ≥3/4 metrics passing

    # Save metrics
    metrics_file = output_dir / "metrics.json"
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=2)

    # Print summary
    print("\n" + "=" * 60)
    print("TASK 5 EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Mechanism Recall: {recall:.1%} ({'PASS' if passes['mechanism_recall'] else 'FAIL'})")
    print(f"Intervention Ranking (τ): {tau:.2f} ({'PASS' if passes['intervention_ranking'] else 'FAIL'})")
    print(f"Citation Count: {total_count} ({'PASS' if passes['citation_count'] else 'FAIL'})")
    print(f"Primary Research Ratio: {primary_ratio:.1%} ({'PASS' if passes['primary_research_ratio'] else 'FAIL'})")
    print("-" * 60)
    print(f"OVERALL: {'PASS' if metrics['overall_pass'] else 'FAIL'}")
    print("=" * 60)

    return metrics


if __name__ == "__main__":
    main()