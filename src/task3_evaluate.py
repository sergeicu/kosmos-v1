#!/usr/bin/env python3
"""
Task 3: Systems Biology - Evaluation Script

This script calculates evaluation metrics for Task 3 results.
"""

import json
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import pandas as pd
from pathlib import Path


def calculate_gene_recall(identified_degs, ground_truth):
    """% of canonical heat shock genes identified as DEGs"""
    identified_set = set([g.lower() for g in identified_degs])
    canonical_set = set([g.lower() for g in ground_truth["canonical_upregulated_genes"]])
    overlap = identified_set & canonical_set
    recall = len(overlap) / len(canonical_set) if canonical_set else 0
    return recall * 100, list(overlap)


def test_notebook_execution(notebook_path):
    """Can the generated notebook execute without errors?"""
    if not os.path.exists(notebook_path):
        return False, f"Notebook not found: {notebook_path}"

    try:
        with open(notebook_path) as f:
            nb = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        # Execute in the directory containing the notebook
        nb_dir = os.path.dirname(os.path.abspath(notebook_path))
        ep.preprocess(nb, {'metadata': {'path': nb_dir}})
        return True, None
    except Exception as e:
        return False, str(e)


def count_figures(output_dir):
    """Count generated figures"""
    fig_dir = os.path.join(output_dir, "figures")
    if not os.path.exists(fig_dir):
        # Also check for figures in output_dir directly
        if os.path.exists(output_dir):
            figures = [f for f in os.listdir(output_dir)
                      if f.endswith(('.png', '.pdf', '.jpg', '.jpeg', '.svg'))]
            return len(figures)
        return 0

    figures = [f for f in os.listdir(fig_dir)
              if f.endswith(('.png', '.pdf', '.jpg', '.jpeg', '.svg'))]
    return len(figures)


def evaluate_hypotheses(hypotheses, ground_truth_mechanisms):
    """Qualitative: Do hypotheses relate to known mechanisms?"""
    if not hypotheses:
        return 0, "No hypotheses provided"

    score = 0
    evaluations = []

    for i, hyp in enumerate(hypotheses, 1):
        hyp_lower = hyp.lower()
        matched_mechanism = None

        for mechanism in ground_truth_mechanisms:
            if any(word in hyp_lower for word in mechanism.lower().split()):
                score += 1
                matched_mechanism = mechanism
                break

        evaluations.append({
            "hypothesis": hyp,
            "matches_known_mechanism": bool(matched_mechanism),
            "matched_mechanism": matched_mechanism
        })

    quality_score = score / len(hypotheses) * 100 if hypotheses else 0
    return quality_score, evaluations


def parse_kosmos_output(output_file):
    """Parse Kosmos output to extract DEGs, hypotheses, and notebook"""
    if not os.path.exists(output_file):
        return None, None, None, f"Output file not found: {output_file}"

    try:
        with open(output_file, 'r') as f:
            data = json.load(f)

        # This is a placeholder - actual parsing would depend on Kosmos output format
        identified_degs = []
        hypotheses = []
        notebook_path = None

        # Check if result contains structured data
        if isinstance(data, dict):
            # Extract DEGs if available
            if 'differentially_expressed_genes' in data:
                identified_degs = data['differentially_expressed_genes']

            # Extract hypotheses if available
            if 'hypotheses' in data:
                hypotheses = data['hypotheses']

            # Check for notebook path
            if 'notebook' in data:
                notebook_path = data['notebook']

        return identified_degs, hypotheses, notebook_path, None

    except Exception as e:
        return None, None, None, f"Error parsing output: {e}"


def evaluate_task3(kosmos_output_file, ground_truth_file, output_dir="output/task3_results"):
    """Comprehensive evaluation of Task 3 results"""

    # Load ground truth
    with open(ground_truth_file, 'r') as f:
        ground_truth = json.load(f)

    # Parse Kosmos output
    identified_degs, hypotheses, notebook_path, parse_error = parse_kosmos_output(kosmos_output_file)

    # Initialize metrics
    metrics = {
        "gene_recall": 0,
        "code_execution": False,
        "figure_count": 0,
        "hypothesis_quality": 0,
        "parse_error": parse_error
    }

    # Calculate gene recall
    if identified_degs:
        recall, overlap_genes = calculate_gene_recall(identified_degs, ground_truth)
        metrics["gene_recall"] = recall
        metrics["overlapping_genes"] = overlap_genes

    # Test notebook execution
    if notebook_path:
        success, error = test_notebook_execution(notebook_path)
        metrics["code_execution"] = success
        if not success:
            metrics["notebook_error"] = error
    else:
        metrics["notebook_error"] = "No notebook found in output"

    # Count figures
    metrics["figure_count"] = count_figures(output_dir)

    # Evaluate hypotheses
    if hypotheses:
        quality_score, evaluations = evaluate_hypotheses(hypotheses, ground_truth["known_mechanisms"])
        metrics["hypothesis_quality"] = quality_score
        metrics["hypothesis_evaluations"] = evaluations
        metrics["num_hypotheses"] = len(hypotheses)
    else:
        metrics["hypothesis_error"] = "No hypotheses found in output"
        metrics["num_hypotheses"] = 0

    # Determine pass/fail for each metric
    metrics["gene_recall_pass"] = metrics["gene_recall"] >= 66
    metrics["code_execution_pass"] = metrics["code_execution"] is True
    metrics["figure_count_pass"] = metrics["figure_count"] >= 2
    metrics["hypothesis_quality_pass"] = metrics["hypothesis_quality"] >= 50

    # Overall pass if at least 3/4 metrics pass
    passing_metrics = sum([
        metrics["gene_recall_pass"],
        metrics["code_execution_pass"],
        metrics["figure_count_pass"],
        metrics["hypothesis_quality_pass"]
    ])
    metrics["overall_pass"] = passing_metrics >= 3

    return metrics


def main():
    """Run evaluation"""
    print("Evaluating Task 3 results...")

    kosmos_output = "output/task3_results/kosmos_raw_output.json"
    ground_truth = "input/task3_ground_truth.json"

    metrics = evaluate_task3(kosmos_output, ground_truth)

    # Save metrics
    with open("output/task3_results/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # Print summary
    print("\n=== Task 3 Evaluation Results ===")
    print(f"Gene Recall: {metrics['gene_recall']:.1f}% (Target: ≥66%) - {'PASS' if metrics['gene_recall_pass'] else 'FAIL'}")
    print(f"Code Execution: {metrics['code_execution']} (Target: True) - {'PASS' if metrics['code_execution_pass'] else 'FAIL'}")
    print(f"Figure Count: {metrics['figure_count']} (Target: ≥2) - {'PASS' if metrics['figure_count_pass'] else 'FAIL'}")
    print(f"Hypothesis Quality: {metrics['hypothesis_quality']:.1f}% (Target: ≥50%) - {'PASS' if metrics['hypothesis_quality_pass'] else 'FAIL'}")
    print(f"\nOverall: {'PASS' if metrics['overall_pass'] else 'FAIL'}")

    if metrics.get("parse_error"):
        print(f"\nParse Error: {metrics['parse_error']}")


if __name__ == "__main__":
    main()