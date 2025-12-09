# Task 1: Cancer Genomics - LITERATURE Job

## Objective
Test Kosmos LITERATURE capability for synthesizing recent research on KRAS-mutant pancreatic cancer to support grant proposal background sections.

## Context
You are running Experiment 1 of 5 in a Kosmos pilot study funded by Schmidt Sciences. This task tests if Kosmos can provide high-quality literature synthesis that computational biologists would use when writing research proposals.

## Your Task

### 1. Run Kosmos LITERATURE Query

**Query:**
```
What are the most promising targetable dependencies in KRAS-mutant pancreatic cancer identified in the last 3 years, and what mechanisms underlie resistance to current targeted therapies?
```

**Use Edison API:**
- Job type: `JobNames.LITERATURE`
- Expected runtime: ~15 minutes
- Cost: ~$200/run

### 2. Parse Results

Extract from Kosmos output:
- **Identified targets:** List of protein/pathway names
- **Resistance mechanisms:** List of mechanisms
- **Citations:** All cited papers (with DOIs if available)
- **Key figures:** Any relevant data visualizations

Save to: `output/task1_results/kosmos_raw_output.json`

### 3. Compare to Ground Truth

**Ground Truth - Known KRAS-mutant PDAC targets (as of 2024):**
```json
{
  "known_targets": ["SHP2", "SOS1", "MRTX1133", "MRTX849", "RM-018"],
  "known_resistance_mechanisms": [
    "KRAS G12D/V bypass signaling",
    "MEK reactivation",
    "RTK-mediated escape",
    "Adaptive metabolic rewiring"
  ],
  "key_papers": [
    "10.1038/s41586-023-06747-5",  // MRTX1133 Nature 2023
    "10.1016/j.ccell.2023.01.003",  // SHP2 resistance Cancer Cell 2023
    "10.1126/science.adg7943"  // Pan-KRAS Science 2023
  ]
}
```

Save to: `input/task1_ground_truth.json`

### 4. Calculate Metrics

Run automated evaluation:

```python
# File: src/task1_evaluate.py

def calculate_target_recall(identified, ground_truth):
    """% of known targets found by Kosmos"""
    overlap = set(identified) & set(ground_truth["known_targets"])
    return len(overlap) / len(ground_truth["known_targets"])

def validate_citations(citations, sample_size=5):
    """Spot-check random citations exist"""
    import random
    sample = random.sample(citations, min(sample_size, len(citations)))
    valid_count = 0
    for citation in sample:
        if verify_doi_exists(citation):  # Use CrossRef API
            valid_count += 1
    return valid_count / len(sample)

def verify_doi_exists(doi):
    """Check if DOI resolves via CrossRef API"""
    import requests
    response = requests.get(f"https://api.crossref.org/works/{doi}")
    return response.status_code == 200
```

**Metrics to calculate:**
- **Target recall:** % of `known_targets` identified (target: ≥75%)
- **Citation count:** Total citations (target: ≥20)
- **Citation validity:** % of spot-checked citations that exist (target: 100%)
- **Key paper coverage:** % of `key_papers` cited (target: ≥66%)

Save to: `output/task1_results/metrics.json`

### 5. Generate Report

Create: `output/task1_results/task1_report.md`

**Template:**
```markdown
# Task 1: Cancer Genomics - Results

## Execution Summary
- **Start time:** {timestamp}
- **End time:** {timestamp}
- **Duration:** {minutes}
- **Cost:** $200

## Kosmos Query
{query text}

## Ground Truth Comparison

### Targets Identified
| Target | Found by Kosmos | In Ground Truth |
|--------|----------------|-----------------|
| SHP2 | ✓/✗ | ✓ |
| ... | ... | ... |

**Recall:** {X}% ({Y}/{Z} targets found)

### Resistance Mechanisms
| Mechanism | Found | In Ground Truth |
|-----------|-------|-----------------|
| ... | ... | ... |

### Citations
- **Total citations:** {N}
- **Spot-check sample:** {5} random citations
- **Valid citations:** {M}/5 (100% target)
- **Fabricated citations:** {list any that failed verification}

### Key Paper Coverage
| DOI | Cited by Kosmos |
|-----|-----------------|
| 10.1038/s41586-023-06747-5 | ✓/✗ |
| ... | ... |

## Metrics

| Metric | Target | Actual | Pass/Fail |
|--------|--------|--------|-----------|
| Target recall | ≥75% | {X}% | PASS/FAIL |
| Citation count | ≥20 | {N} | PASS/FAIL |
| Citation validity | 100% | {Y}% | PASS/FAIL |
| Key paper coverage | ≥66% | {Z}% | PASS/FAIL |

## Overall Assessment
**PASS/FAIL:** {based on ≥3/4 metrics passing}

## Raw Outputs
- Kosmos response: `kosmos_raw_output.json`
- Metrics: `metrics.json`
- Execution log: `../logs/task1_execution.log`

## Notes
{Any observations about quality, edge cases, failures}
```

## File Naming Convention
- Source code: `src/task1_*.py` or `src/task1_*.sh`
- Input data: `input/task1_ground_truth.json`
- Outputs: `output/task1_results/*`
- Logs: `logs/task1_execution.log`

## Success Criteria
- [ ] Kosmos job completes successfully
- [ ] Raw output saved to JSON
- [ ] All 4 metrics calculated
- [ ] Report generated
- [ ] ≥3/4 metrics pass targets
- [ ] Zero fabricated citations

## If Job Fails
1. Save error message to `logs/task1_error.log`
2. Document failure mode in report
3. Mark overall assessment as FAIL
4. Still generate partial report with available data

## Tools Available
- Edison Python SDK (for Kosmos API)
- requests (for citation verification)
- pytest (for test assertions)
- Standard Python scientific stack (pandas, numpy, json)

## Budget
$200 for this experiment (1 Kosmos LITERATURE run)

## Timeline
Target completion: 30 minutes (15 min Kosmos + 15 min evaluation)
