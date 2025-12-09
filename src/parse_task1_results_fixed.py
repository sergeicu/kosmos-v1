#!/usr/bin/env python3
"""
Parse Task 1 results and evaluate against ground truth (Fixed version)
"""

import json
import re
import requests
import random
from datetime import datetime

# Load ground truth
with open("input/task1_ground_truth.json", "r") as f:
    ground_truth = json.load(f)

# Load Kosmos results
with open("output/task1_results/kosmos_raw_output.json", "r") as f:
    kosmos_data = json.load(f)

# Extract the answer
task = kosmos_data.get("task", "")
if isinstance(task, str):
    # Parse the task object to extract answer
    import ast
    try:
        task_dict = ast.literal_eval(task)
        answer = task_dict.get("answer", "")
    except:
        # Find answer in the string
        answer_match = re.search(r"answer='([^']+)", task)
        if answer_match:
            answer = answer_match.group(1)
        else:
            answer = task
else:
    answer = task.get("answer", "")

print(f"Answer length: {len(answer)} characters")

# Parse identified targets from answer - simpler approach
identified_targets = []

# Known target names and their common variations
target_variations = {
    "SHP2": ["SHP2", "ptpn11"],
    "SOS1": ["SOS1", "sos1"],
    "MRTX1133": ["MRTX1133", "mrtx1133"],
    "MRTX849": ["MRTX849", "mrtx849", "adagrasib"],
    "RM-018": ["RM-018", "rm-018"]
}

# Search for each target
for target, variations in target_variations.items():
    for var in variations:
        if var in answer.lower() or re.search(r'\b' + re.escape(var) + r'\b', answer, re.IGNORECASE):
            identified_targets.append(target)
            break

# Remove duplicates
identified_targets = list(set(identified_targets))

print(f"\nIdentified targets: {identified_targets}")

# Parse resistance mechanisms
resistance_mechanisms = []

# Known resistance mechanisms from ground truth
known_mechanisms = ground_truth["known_resistance_mechanisms"]
mechanism_keywords = [
    ("KRAS G12D/V bypass signaling", ["bypass", "kras.*bypass", "wild-type.*ras"]),
    ("MEK reactivation", ["mek.*reactivation", "erk.*reactivation", "reactivation"]),
    ("RTK-mediated escape", ["rtk", "receptor.*tyrosine.*kinase", "escape"]),
    ("Adaptive metabolic rewiring", ["metabolic", "rewir", "autophagy", "macropinocytosis"])
]

for mechanism_name, keywords in mechanism_keywords:
    for keyword in keywords:
        if re.search(keyword, answer, re.IGNORECASE):
            resistance_mechanisms.append(mechanism_name)
            break

print(f"Resistance mechanisms: {resistance_mechanisms}")

# Parse citations (look for DOIs and NCT IDs)
doi_pattern = r'https://doi\.org/10\.\d+/[^\s,)]+'
dois = re.findall(doi_pattern, answer)

# Also look for DOI numbers without full URL
doi_num_pattern = r'10\.\d+/[^\s,)]+'
doi_nums = re.findall(doi_num_pattern, answer)

nct_pattern = r'NCT\d+'
nct_ids = re.findall(nct_pattern, answer)

citations = []
for doi in dois:
    # Extract just the DOI part
    doi_clean = doi.split('https://doi.org/')[-1] if 'https://doi.org/' in doi else doi
    citations.append(doi_clean)
for doi_num in doi_nums:
    if doi_num not in citations:
        citations.append(doi_num)
citations.extend(nct_ids)

# Remove duplicates
citations = list(set(citations))

print(f"\nCitations found: {len(citations)}")
print(f"DOI citations: {len(dois) + len(doi_nums)}")
print(f"NCT trial IDs: {len(nct_ids)}")

# Save parsed results
parsed_results = {
    "identified_targets": identified_targets,
    "resistance_mechanisms": resistance_mechanisms,
    "citations": citations,
    "doi_citations": citations[:len(dois)+len(doi_nums)],
    "nct_trials": nct_ids,
    "total_citations": len(citations)
}

with open("output/task1_results/parsed_results.json", "w") as f:
    json.dump(parsed_results, f, indent=2)

print(f"\nParsed results saved to output/task1_results/parsed_results.json")

# Calculate metrics
def verify_doi_exists(doi):
    """Check if DOI resolves via CrossRef API"""
    try:
        response = requests.get(f"https://api.crossref.org/works/{doi}")
        return response.status_code == 200
    except:
        return False

# Target recall
overlap_targets = set(identified_targets) & set(ground_truth["known_targets"])
target_recall = len(overlap_targets) / len(ground_truth["known_targets"])

print(f"\n=== METRICS ===")
print(f"Target recall: {target_recall:.1%} ({len(overlap_targets)}/{len(ground_truth['known_targets'])} targets found)")
print(f"Targets found: {list(overlap_targets)}")
print(f"Targets missed: {set(ground_truth['known_targets']) - overlap_targets}")

# Citation count
citation_count = len(citations)
print(f"\nCitation count: {citation_count} (target: ≥20)")

# Citation validity - check DOI validity
if citations:
    # Only check DOI citations, not NCT IDs
    doi_citations = [c for c in citations if c.startswith('10.')]
    if doi_citations:
        sample_size = min(5, len(doi_citations))
        sample = random.sample(doi_citations, sample_size)
        valid_count = 0

        for citation in sample:
            if verify_doi_exists(citation):
                valid_count += 1
                print(f"  ✓ {citation} - Valid")
            else:
                print(f"  ✗ {citation} - Invalid/Fabricated")

        citation_validity = valid_count / sample_size
        print(f"\nCitation validity (DOIs only): {citation_validity:.1%} ({valid_count}/{sample_size} verified)")
    else:
        citation_validity = 1.0  # Assume NCT IDs are valid
        print(f"\nCitation validity: 100% (all citations are NCT trial IDs)")
else:
    citation_validity = 0.0
    print("\nCitation validity: 0% (no citations found)")

# Key paper coverage - check for ground truth DOIs
doi_citations = set([c for c in citations if c.startswith('10.')])
key_paper_overlap = doi_citations & set(ground_truth["key_papers"])
key_paper_coverage = len(key_paper_overlap) / len(ground_truth["key_papers"])
print(f"\nKey paper coverage: {key_paper_coverage:.1%} ({len(key_paper_overlap)}/{len(ground_truth['key_papers'])} key papers found)")
print(f"Key papers found: {list(key_paper_overlap)}")

# Save metrics
metrics = {
    "target_recall": target_recall,
    "citation_count": citation_count,
    "citation_validity": citation_validity,
    "key_paper_coverage": key_paper_coverage,
    "targets_found": list(overlap_targets),
    "targets_missed": list(set(ground_truth["known_targets"]) - overlap_targets),
    "key_papers_found": list(key_paper_overlap),
    "resistance_mechanisms_found": resistance_mechanisms,
    "total_doi_citations": len(doi_citations),
    "total_nct_citations": len(nct_ids),
    "evaluation_timestamp": datetime.now().isoformat()
}

with open("output/task1_results/metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print(f"\nMetrics saved to output/task1_results/metrics.json")

# Determine pass/fail
target_recall_pass = target_recall >= 0.75
citation_count_pass = citation_count >= 20
citation_validity_pass = citation_validity == 1.0
key_paper_coverage_pass = key_paper_coverage >= 0.66

passed_metrics = sum([target_recall_pass, citation_count_pass, citation_validity_pass, key_paper_coverage_pass])
overall_assessment = "PASS" if passed_metrics >= 3 else "FAIL"

print(f"\n=== FINAL ASSESSMENT ===")
print(f"Target recall (≥75%): {'PASS' if target_recall_pass else 'FAIL'} - {target_recall:.1%}")
print(f"Citation count (≥20): {'PASS' if citation_count_pass else 'FAIL'} - {citation_count}")
print(f"Citation validity (100%): {'PASS' if citation_validity_pass else 'FAIL'} - {citation_validity:.1%}")
print(f"Key paper coverage (≥66%): {'PASS' if key_paper_coverage_pass else 'FAIL'} - {key_paper_coverage:.1%}")
print(f"\nOverall: {overall_assessment} ({passed_metrics}/4 metrics passing)")

# Update todo list
print(f"\n=== TASK COMPLETION STATUS ===")
print(f"✓ Kosmos query completed")
print(f"✓ Results collected and parsed")
print(f"✓ Metrics calculated")
print(f"✓ Overall assessment: {overall_assessment}")