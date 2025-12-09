#!/usr/bin/env python3
"""
Task 1 Evaluation Script
Calculate metrics for Task 1 results
"""

import json
import requests
import random
from pathlib import Path


def calculate_target_recall(identified, ground_truth):
    """% of known targets found by Kosmos"""
    overlap = set(identified) & set(ground_truth["known_targets"])
    return len(overlap) / len(ground_truth["known_targets"])


def validate_citations(citations, sample_size=5):
    """Spot-check random citations exist"""
    sample = random.sample(citations, min(sample_size, len(citations)))
    valid_count = 0
    for citation in sample:
        if verify_doi_exists(citation):
            valid_count += 1
    return valid_count / len(sample)


def verify_doi_exists(doi):
    """Check if DOI resolves via CrossRef API"""
    try:
        response = requests.get(f"https://api.crossref.org/works/{doi}")
        return response.status_code == 200
    except:
        return False


def main():
    # Load ground truth
    with open("input/task1_ground_truth.json", "r") as f:
        ground_truth = json.load(f)

    # Try to load Kosmos results
    kosmos_file = Path("output/task1_results/kosmos_raw_output.json")

    if kosmos_file.exists():
        with open(kosmos_file, "r") as f:
            kosmos_results = json.load(f)

        # For now, create dummy parsed results
        # This would need to be updated based on actual Kosmos response format
        parsed_results = {
            "identified_targets": [],  # Extract from kosmos_results
            "resistance_mechanisms": [],  # Extract from kosmos_results
            "citations": [],  # Extract from kosmos_results
            "key_figures": []  # Extract from kosmos_results
        }

        # Calculate metrics
        target_recall = calculate_target_recall(parsed_results["identified_targets"], ground_truth)

        if parsed_results["citations"]:
            citation_count = len(parsed_results["citations"])
            citation_validity = validate_citations(parsed_results["citations"])
        else:
            citation_count = 0
            citation_validity = 0.0

        # Key paper coverage
        overlap = set(parsed_results["citations"]) & set(ground_truth["key_papers"])
        key_paper_coverage = len(overlap) / len(ground_truth["key_papers"])

        metrics = {
            "target_recall": target_recall,
            "citation_count": citation_count,
            "citation_validity": citation_validity,
            "key_paper_coverage": key_paper_coverage
        }

        # Save metrics
        with open("output/task1_results/metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)

        print(f"Metrics calculated:")
        print(f"  Target recall: {target_recall:.1%}")
        print(f"  Citation count: {citation_count}")
        print(f"  Citation validity: {citation_validity:.1%}")
        print(f"  Key paper coverage: {key_paper_coverage:.1%}")

        # Determine pass/fail
        target_recall_pass = target_recall >= 0.75
        citation_count_pass = citation_count >= 20
        citation_validity_pass = citation_validity == 1.0
        key_paper_coverage_pass = key_paper_coverage >= 0.66

        passed_metrics = sum([target_recall_pass, citation_count_pass, citation_validity_pass, key_paper_coverage_pass])
        overall_assessment = "PASS" if passed_metrics >= 3 else "FAIL"

        print(f"\nOverall Assessment: {overall_assessment} ({passed_metrics}/4 metrics passing)")

    else:
        print(f"Kosmos results not found at {kosmos_file}")
        print("Task may still be running. Check the task ID:")

        try:
            with open("output/task1_results/task_id.txt", "r") as f:
                task_id = f.read().strip()
            print(f"Task ID: {task_id}")
        except:
            print("Task ID not found")


if __name__ == "__main__":
    main()