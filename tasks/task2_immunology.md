# Task 2: Immunology - PRECEDENT Job

## Objective
Test Kosmos PRECEDENT capability for identifying prior work on mRNA cancer vaccines to validate hypothesis novelty for grant proposals.

## Context
You are running Experiment 2 of 5 in a Kosmos pilot study. This task tests if Kosmos can accurately determine if research has been done before, critical for justifying proposal novelty.

## Your Task

### 1. Run Kosmos PRECEDENT Query

**Query:**
```
Has anyone developed mRNA vaccines targeting solid tumor neoantigens using patient-specific mutation profiles, and what were the clinical trial outcomes?
```

**Use Edison API:**
- Job type: `JobNames.PRECEDENT`
- Expected runtime: ~15 minutes
- Cost: ~$200/run
- Should search ClinicalTrials.gov database

### 2. Parse Results

Extract from Kosmos output:
- **Precedent exists:** Yes/No
- **Clinical trial IDs:** List of NCT numbers
- **Trial outcomes:** Summary of results for each trial
- **Key institutions:** Organizations conducting trials
- **Citations:** Papers describing the trials

Save to: `output/task2_results/kosmos_raw_output.json`

### 3. Compare to Ground Truth

**Ground Truth - Known mRNA neoantigen vaccine trials:**
```json
{
  "precedent_exists": true,
  "known_trials": [
    {
      "nct_id": "NCT02410733",
      "name": "BNT111",
      "sponsor": "BioNTech",
      "indication": "Melanoma",
      "approach": "Personalized neoantigen mRNA",
      "status": "Completed",
      "outcome": "Safe, induced immune responses"
    },
    {
      "nct_id": "NCT03313778",
      "name": "mRNA-4157",
      "sponsor": "Moderna",
      "indication": "Solid tumors",
      "approach": "Personalized neoantigen mRNA (up to 34 neoantigens)",
      "status": "Active",
      "outcome": "Combined with pembrolizumab, reduced recurrence in melanoma"
    },
    {
      "nct_id": "NCT03639714",
      "name": "SLATE",
      "sponsor": "Gritstone",
      "indication": "NSCLC, other solid tumors",
      "approach": "Shared + personalized neoantigens",
      "status": "Completed",
      "outcome": "Immune responses observed"
    }
  ],
  "key_papers": [
    "10.1038/s41586-021-03368-8",  // Moderna Phase 1 Nature 2021
    "10.1038/s41586-022-05400-5"   // BioNTech personalized vaccine Nature 2022
  ]
}
```

Save to: `input/task2_ground_truth.json`

### 4. Calculate Metrics

Run automated evaluation:

```python
# File: src/task2_evaluate.py

def calculate_trial_recall(identified_ncts, ground_truth):
    """% of known trials found by Kosmos"""
    identified_set = set(extract_nct_ids(identified_ncts))
    known_set = set([t["nct_id"] for t in ground_truth["known_trials"]])
    overlap = identified_set & known_set
    return len(overlap) / len(known_set)

def extract_nct_ids(text_or_list):
    """Extract NCT IDs from Kosmos output"""
    import re
    if isinstance(text_or_list, str):
        return re.findall(r'NCT\d{8}', text_or_list)
    return text_or_list

def verify_precedent_accuracy(kosmos_answer, ground_truth):
    """Binary: Did Kosmos correctly say Yes/No to precedent?"""
    return kosmos_answer == ground_truth["precedent_exists"]

def check_outcome_completeness(kosmos_output, ground_truth):
    """Does Kosmos provide outcome data for trials?"""
    # Check if outcome info is present for identified trials
    has_outcomes = "outcome" in kosmos_output.lower() or "result" in kosmos_output.lower()
    return has_outcomes
```

**Metrics to calculate:**
- **Trial recall:** % of `known_trials` NCT IDs identified (target: ≥66%, i.e., 2/3)
- **Precedent accuracy:** Correct yes/no answer (target: 100%)
- **Outcome completeness:** Includes clinical outcome data (target: True)
- **Key paper coverage:** % of `key_papers` cited (target: ≥50%)

Save to: `output/task2_results/metrics.json`

### 5. Generate Report

Create: `output/task2_results/task2_report.md`

**Template:**
```markdown
# Task 2: Immunology - Results

## Execution Summary
- **Start time:** {timestamp}
- **End time:** {timestamp}
- **Duration:** {minutes}
- **Cost:** $200

## Kosmos Query
{query text}

## Ground Truth Comparison

### Precedent Question
- **Kosmos answer:** {Yes/No}
- **Ground truth:** {Yes}
- **Correct:** ✓/✗

### Clinical Trials Identified
| NCT ID | Found by Kosmos | In Ground Truth | Sponsor | Outcome Reported |
|--------|----------------|-----------------|---------|------------------|
| NCT02410733 | ✓/✗ | ✓ | BioNTech | ✓/✗ |
| NCT03313778 | ✓/✗ | ✓ | Moderna | ✓/✗ |
| NCT03639714 | ✓/✗ | ✓ | Gritstone | ✓/✗ |
| {any extras} | ✓ | ✗ | ... | ... |

**Recall:** {X}% ({Y}/{Z} trials found)

### Outcome Data Quality
{Qualitative assessment of whether Kosmos provided meaningful outcome summaries}

Examples:
- NCT02410733: "{Kosmos outcome summary}"
- ...

### Citations
| DOI | Purpose | Cited by Kosmos |
|-----|---------|-----------------|
| 10.1038/s41586-021-03368-8 | Moderna Phase 1 | ✓/✗ |
| 10.1038/s41586-022-05400-5 | BioNTech vaccine | ✓/✗ |

## Metrics

| Metric | Target | Actual | Pass/Fail |
|--------|--------|--------|-----------|
| Trial recall | ≥66% | {X}% | PASS/FAIL |
| Precedent accuracy | 100% | {Y}% | PASS/FAIL |
| Outcome completeness | True | {T/F} | PASS/FAIL |
| Key paper coverage | ≥50% | {Z}% | PASS/FAIL |

## Overall Assessment
**PASS/FAIL:** {based on all 4 metrics passing}

## Research Gap Identification
{If Kosmos identified any gaps in the existing work - important for proposals}

## Raw Outputs
- Kosmos response: `kosmos_raw_output.json`
- Metrics: `metrics.json`
- Execution log: `../logs/task2_execution.log`

## Notes
{Observations about search scope, database coverage, false positives}
```

## File Naming Convention
- Source code: `src/task2_*.py` or `src/task2_*.sh`
- Input data: `input/task2_ground_truth.json`
- Outputs: `output/task2_results/*`
- Logs: `logs/task2_execution.log`

## Success Criteria
- [ ] Kosmos job completes successfully
- [ ] Raw output saved to JSON
- [ ] All 4 metrics calculated
- [ ] Report generated
- [ ] All 4 metrics pass targets
- [ ] Correct binary precedent answer (Yes)

## If Job Fails
1. Save error message to `logs/task2_error.log`
2. Document failure mode in report
3. Mark overall assessment as FAIL
4. Still generate partial report with available data

## Tools Available
- Edison Python SDK (for Kosmos API)
- requests (for clinical trial API verification)
- pytest (for test assertions)
- Standard Python scientific stack

## Budget
$200 for this experiment (1 Kosmos PRECEDENT run)

## Timeline
Target completion: 30 minutes (15 min Kosmos + 15 min evaluation)

## Additional Notes
- PRECEDENT searches should include ClinicalTrials.gov
- May also search PubMed, bioRxiv (verify in output)
- False positives (extra trials found) are acceptable if they're relevant
- Focus on precision: are the identified trials actually about personalized mRNA neoantigen vaccines?
