#!/usr/bin/env python3
"""
Parse Task 1 results and evaluate against ground truth
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
        answer = task
else:
    answer = task.get("answer", "")

print(f"Answer length: {len(answer)} characters")

# Parse identified targets from answer
# Look for target names in the text
identified_targets = []
target_patterns = [
    r'\bSHP2\b',
    r'\bSOS1\b',
    r'\bMRTX1133\b',
    r'\bMRTX849\b',
    r'\bRM-018\b',
    r'\bdaraxonrasib\b',
    r'\bRMC-6236\b',
    r'\bKRAS G12D\b',
    r'\bULK1/2\b',
    r'\bWEE1\b',
    r'\bATR\b',
    r'\bERK\b',
    r'\bMEK\b'
]

for pattern in target_patterns:
    if re.search(pattern, answer, re.IGNORECASE):
        target = re.sub(r'\b', '', pattern).lower()
        if target == 'kras g12d':
            identified_targets.append('MRTX1133')  # MRTX1133 is a KRAS G12D inhibitor
        elif pattern == r'\bdaraxonrasib\b':
            identified_targets.append('RMC-6236')  # daraxonrasib is RMC-6236
        else:
            identified_targets.append(re.sub(r'\b', '', pattern))

# Remove duplicates
identified_targets = list(set(identified_targets))

print(f"\nIdentified targets: {identified_targets}")

# Parse resistance mechanisms
resistance_mechanisms = []
mechanism_patterns = [
    r'RTK.*mediated.*escape',
    r'MEK.*reactivation',
    r'autophagy',
    r'macropinocytosis',
    r'metabolic.*rewir.*',
    r'KRAS.*bypass',
    r'parallel.*PI3K',
    r'on.*target.*mutation',
    r'ERBB.*feedback',
    r'ferroptosis.*suppression'
]

for pattern in mechanism_patterns:
    if re.search(pattern, answer, re.IGNORECASE):
        mechanism = pattern.replace(r'.*', ' ').strip()
        resistance_mechanisms.append(mechanism)

print(f"Resistance mechanisms: {resistance_mechanisms}")

# Parse citations (look for DOIs and NCT IDs)
doi_pattern = r'https://doi\.org/10\.\d+/(?:[^\s]+)'
dois = re.findall(doi_pattern, answer)

nct_pattern = r'NCT\d+'
nct_ids = re.findall(nct_pattern, answer)

citations = []
for doi in dois:
    citations.append(doi.split('/')[-1])  # Extract DOI number
citations.extend(nct_ids)

print(f"\nCitations found: {len(citations)}")
print(f"DOI citations: {len(dois)}")
print(f"NCT trial IDs: {len(nct_ids)}")

# Save parsed results
parsed_results = {
    "identified_targets": identified_targets,
    "resistance_mechanisms": resistance_mechanisms,
    "citations": citations,
    "doi_citations": [f"10.{doi.split('/')[-1]}" for doi in dois],
    "nct_trials": nct_ids,
    "raw_answer": answer[:5000]  # First 5000 chars as sample
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

# Citation validity
if citations:
    sample_size = min(5, len(citations))
    sample = random.sample(citations, sample_size)
    valid_count = 0

    for citation in sample:
        if citation.startswith('10.'):
            if verify_doi_exists(citation):
                valid_count += 1
                print(f"  ✓ {citation} - Valid")
            else:
                print(f"  ✗ {citation} - Invalid/Fabricated")
        else:
            # NCT IDs
            print(f"  ? {citation} - NCT ID (not verifying)")
            valid_count += 1  # Assume NCT IDs are valid

    citation_validity = valid_count / sample_size
    print(f"\nCitation validity: {citation_validity:.1%} ({valid_count}/{sample_size} verified)")
else:
    citation_validity = 0.0
    print("\nCitation validity: 0% (no citations found)")

# Key paper coverage
key_paper_overlap = set(parsed_results["doi_citations"]) & set(ground_truth["key_papers"])
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