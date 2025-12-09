# Task 5: Neuroscience - LITERATURE Job

## Objective
Test Kosmos LITERATURE capability for cross-domain synthesis (microbiology + neuroscience) to support grant proposals on the gut-brain axis.

## Context
You are running Experiment 5 of 5 in a Kosmos pilot study. This task tests if Kosmos can synthesize literature across multiple disciplines and rank therapeutic interventions.

## Your Task

### 1. Run Kosmos LITERATURE Query

**Query:**
```
What circuit-level mechanisms link gut microbiome dysbiosis to Parkinson's disease pathology, and which mechanisms are most amenable to therapeutic intervention? Rank potential interventions by current feasibility (clinical readiness, mechanistic understanding, and safety profile).
```

**Use Edison API:**
- Job type: `JobNames.LITERATURE`
- Expected runtime: ~15 minutes
- Cost: ~$200/run

### 2. Parse Results

Extract from Kosmos output:
- **Identified mechanisms:** List of pathways linking microbiome to PD
- **Circuit-level details:** Specific neural pathways (e.g., vagus nerve, enteric nervous system)
- **Ranked interventions:** List with rationale for ranking
- **Citations:** All cited papers
- **Key figures/tables:** Any relevant visualizations

Save to: `output/task5_results/kosmos_raw_output.json`

### 3. Compare to Ground Truth

**Ground Truth - Known gut-brain-PD mechanisms (as of 2024):**
```json
{
  "established_mechanisms": [
    {
      "name": "Alpha-synuclein propagation via vagus nerve",
      "description": "Misfolded α-syn travels from enteric neurons to brain via vagal pathway",
      "evidence_strength": "Strong (animal models + human epidemiology)",
      "key_papers": ["10.1002/ana.24448", "10.1001/jamaneurol.2014.3865"]
    },
    {
      "name": "LPS-induced neuroinflammation",
      "description": "Bacterial LPS from gut triggers systemic inflammation, activates microglia",
      "evidence_strength": "Moderate (animal models, correlational in humans)",
      "key_papers": ["10.1038/s41586-020-03186-4", "10.1016/j.neuron.2020.01.033"]
    },
    {
      "name": "Short-chain fatty acid (SCFA) depletion",
      "description": "Reduced butyrate/propionate impairs BBB integrity and neuroprotection",
      "evidence_strength": "Moderate (emerging)",
      "key_papers": ["10.1038/s41531-020-00156-5"]
    },
    {
      "name": "Gut-derived neurotransmitter alterations",
      "description": "Dysbiosis reduces serotonin/dopamine precursors, affecting brain levels",
      "evidence_strength": "Weak (mostly preclinical)",
      "key_papers": ["10.1016/j.cell.2015.09.016"]
    }
  ],
  "known_interventions": [
    {
      "intervention": "GLP-1 receptor agonists",
      "mechanism": "Neuroprotection, anti-inflammation, may modulate microbiome",
      "clinical_readiness": "High (Phase 3 trials ongoing for PD)",
      "safety": "Well-established (approved for diabetes)",
      "key_trials": ["NCT03659682"]
    },
    {
      "intervention": "Probiotic supplementation",
      "mechanism": "Restore beneficial bacteria, increase SCFAs, reduce inflammation",
      "clinical_readiness": "Medium (small Phase 2 trials completed)",
      "safety": "High (GRAS status)",
      "key_trials": ["NCT03528421"]
    },
    {
      "intervention": "Fecal microbiota transplant (FMT)",
      "mechanism": "Restore healthy microbiome, reduce dysbiosis",
      "clinical_readiness": "Low (preclinical + case reports only)",
      "safety": "Medium (infection risk, regulatory hurdles)",
      "key_trials": ["Preclinical only"]
    },
    {
      "intervention": "Vagotomy (surgical)",
      "mechanism": "Block α-syn propagation pathway",
      "clinical_readiness": "Observational only (not interventional)",
      "safety": "Low (surgical risks, irreversible)",
      "key_trials": ["Epidemiological studies only"]
    }
  ],
  "expected_ranking_order": [
    "GLP-1 agonists",  // Highest feasibility
    "Probiotic supplementation",
    "Fecal microbiota transplant",
    "Vagotomy"  // Lowest feasibility
  ]
}
```

Save to: `input/task5_ground_truth.json`

### 4. Calculate Metrics

Run automated evaluation:

```python
# File: src/task5_evaluate.py

def calculate_mechanism_recall(identified, ground_truth):
    """% of established mechanisms identified by Kosmos"""
    # Fuzzy matching on mechanism names
    identified_lower = [m.lower() for m in identified]
    gt_mechanisms = [m["name"].lower() for m in ground_truth["established_mechanisms"]]

    overlap = 0
    for gt_mech in gt_mechanisms:
        # Check if any identified mechanism contains key terms
        key_terms = gt_mech.split()[:2]  # E.g., "alpha-synuclein propagation"
        if any(all(term in id_mech for term in key_terms) for id_mech in identified_lower):
            overlap += 1

    return overlap / len(gt_mechanisms)

def evaluate_intervention_ranking(kosmos_ranking, expected_order):
    """Spearman correlation or Kendall's tau for ranking quality"""
    from scipy.stats import kendalltau

    # Map intervention names to positions
    kosmos_positions = {intervention: i for i, intervention in enumerate(kosmos_ranking)}
    expected_positions = {intervention: i for i, intervention in enumerate(expected_order)}

    # Get overlapping interventions
    common = set(kosmos_positions.keys()) & set(expected_positions.keys())
    if len(common) < 2:
        return 0  # Can't compute correlation with <2 items

    kosmos_ranks = [kosmos_positions[item] for item in common]
    expected_ranks = [expected_positions[item] for item in common]

    tau, p_value = kendalltau(kosmos_ranks, expected_ranks)
    return tau  # Range: -1 to 1, higher is better

def count_primary_research_citations(citations):
    """% of citations that are primary research (not reviews)"""
    # Heuristic: check journal names or article types if available
    # For now, assume citations list has 'type' field
    if not citations:
        return 0

    primary = [c for c in citations if c.get("type") == "primary" or "research" in c.get("title", "").lower()]
    return len(primary) / len(citations)
```

**Metrics to calculate:**
- **Mechanism recall:** % of `established_mechanisms` identified (target: ≥75%, i.e., 3/4)
- **Intervention ranking quality:** Kendall's tau correlation (target: ≥0.5)
- **Citation count:** Total primary sources (target: ≥15)
- **Primary research ratio:** % primary research vs. reviews (target: ≥60%)

Save to: `output/task5_results/metrics.json`

### 5. Generate Report

Create: `output/task5_results/task5_report.md`

**Template:**
```markdown
# Task 5: Neuroscience - Results

## Execution Summary
- **Start time:** {timestamp}
- **End time:** {timestamp}
- **Duration:** {minutes}
- **Cost:** $200

## Kosmos Query
{query text}

## Ground Truth Comparison

### Mechanisms Identified
| Mechanism | Found by Kosmos | In Ground Truth | Evidence Strength |
|-----------|----------------|-----------------|-------------------|
| α-synuclein via vagus | ✓/✗ | ✓ | Strong |
| LPS neuroinflammation | ✓/✗ | ✓ | Moderate |
| SCFA depletion | ✓/✗ | ✓ | Moderate |
| Neurotransmitter alterations | ✓/✗ | ✓ | Weak |
| {Additional mechanisms} | ✓ | ✗ | ... |

**Mechanism Recall:** {X}% ({Y}/{Z} established mechanisms found)

### Intervention Ranking

**Kosmos Ranking:**
1. {Intervention 1} - {Rationale}
2. {Intervention 2} - {Rationale}
3. {Intervention 3} - {Rationale}
4. {Intervention 4} - {Rationale}

**Expected Ranking (by feasibility):**
1. GLP-1 agonists
2. Probiotic supplementation
3. Fecal microbiota transplant
4. Vagotomy

**Ranking Quality (Kendall's tau):** {τ value} (target: ≥0.5)

**Analysis:**
{Commentary on whether ranking makes sense:
- Did Kosmos prioritize interventions with clinical trials?
- Did it consider safety profiles?
- Were rationales evidence-based?
}

### Citations
- **Total citations:** {N}
- **Primary research articles:** {M} ({X}% of total, target: ≥60%)
- **Review articles:** {R}
- **Spot-check validation:** {5 random citations checked}
  - Valid: {Y}/5

**Key Papers Coverage:**
| DOI | Topic | Cited by Kosmos |
|-----|-------|-----------------|
| 10.1002/ana.24448 | Vagal propagation | ✓/✗ |
| 10.1001/jamaneurol.2014.3865 | Vagotomy epidemiology | ✓/✗ |
| 10.1038/s41586-020-03186-4 | LPS inflammation | ✓/✗ |
| 10.1016/j.neuron.2020.01.033 | Microbiome-brain axis | ✓/✗ |

## Metrics

| Metric | Target | Actual | Pass/Fail |
|--------|--------|--------|-----------|
| Mechanism recall | ≥75% | {X}% | PASS/FAIL |
| Ranking quality (τ) | ≥0.5 | {Y} | PASS/FAIL |
| Citation count | ≥15 | {N} | PASS/FAIL |
| Primary research ratio | ≥60% | {Z}% | PASS/FAIL |

## Overall Assessment
**PASS/FAIL:** {based on ≥3/4 metrics passing}

## Cross-Domain Synthesis Quality
{Qualitative assessment:
- Did Kosmos successfully integrate microbiology + neuroscience literature?
- Were circuit-level details provided (e.g., vagus nerve, enteric neurons)?
- Did it distinguish correlation from causation?
}

## Therapeutic Feasibility Assessment
{Commentary on intervention ranking rationale:
- Clinical readiness consideration
- Safety profile consideration
- Mechanistic understanding consideration
}

## Raw Outputs
- Kosmos response: `kosmos_raw_output.json`
- Metrics: `metrics.json`
- Execution log: `../logs/task5_execution.log`

## Notes
{Observations about literature coverage, recency bias, missing mechanisms}
```

## File Naming Convention
- Source code: `src/task5_*.py`
- Input data: `input/task5_ground_truth.json`
- Outputs: `output/task5_results/*`
- Logs: `logs/task5_execution.log`

## Success Criteria
- [ ] Kosmos job completes successfully
- [ ] Raw output saved to JSON
- [ ] All 4 metrics calculated
- [ ] Report generated
- [ ] ≥3/4 metrics pass targets
- [ ] Intervention ranking provided with rationale

## If Job Fails
1. Save error message to `logs/task5_error.log`
2. Document failure mode in report
3. Mark overall assessment as FAIL
4. Still generate partial report with available data

## Tools Available
- Edison Python SDK (for Kosmos API)
- requests (for citation verification via CrossRef)
- scipy (for Kendall's tau ranking correlation)
- pytest (for test assertions)
- Standard Python scientific stack

## Budget
$200 for this experiment (1 Kosmos LITERATURE run)

## Timeline
Target completion: 30 minutes (15 min Kosmos + 15 min evaluation)

## Additional Notes
- This tests cross-domain synthesis (microbiology + neuroscience)
- Ranking quality is subjective but Kendall's tau provides quantitative measure
- Primary research vs. reviews distinction is important for proposal writing
- Mechanism names may vary (use fuzzy matching)
- Intervention rationales should cite clinical trials (NCT IDs) if available
