# Task 3: Systems Biology - ANALYSIS Job

## Objective
Test Kosmos ANALYSIS capability for analyzing RNA-seq data to generate testable hypotheses for grant proposals.

## Context
You are running Experiment 3 of 5 in a Kosmos pilot study. This task tests if Kosmos can perform data-driven hypothesis generation from biological datasets.

## Your Task

### 1. Obtain Dataset

**Option A: Use public E. coli heat shock RNA-seq data**
- Source: GEO (Gene Expression Omnibus)
- Suggested: GSE103482 or similar E. coli heat stress dataset
- Format: Counts matrix (genes × samples)
- Samples: ≥6 timepoints or conditions (e.g., 0min, 5min, 10min, 20min, 40min, 60min after heat shock)

**Option B: Simulated test data (if GEO unavailable)**
```python
# File: input/task3_generate_test_data.py
import pandas as pd
import numpy as np

# Canonical heat shock genes with high fold-changes
heat_shock_genes = ["dnaK", "dnaJ", "groEL", "groES", "htpG", "clpB", "ibpA", "ibpB"]
housekeeping = ["rrsA", "gyrA", "recA"]  # Stable expression

# Generate mock counts
np.random.seed(42)
n_genes = 500
samples = ["control_1", "control_2", "heat_1", "heat_2", "heat_3"]

# Simulate data where heat shock genes are upregulated
data = {}
for gene in (heat_shock_genes + housekeeping + [f"gene_{i}" for i in range(n_genes - len(heat_shock_genes) - len(housekeeping))]):
    if gene in heat_shock_genes:
        # High expression in heat samples
        data[gene] = [100, 120] + list(np.random.randint(800, 1200, 3))
    elif gene in housekeeping:
        # Stable across conditions
        data[gene] = list(np.random.randint(400, 600, 5))
    else:
        # Random low expression
        data[gene] = list(np.random.randint(10, 300, 5))

df = pd.DataFrame(data, index=samples).T
df.to_csv("input/task3_ecoli_heatshock.csv")
```

Save to: `input/task3_ecoli_heatshock.csv`

### 2. Run Kosmos ANALYSIS Query

**Query:**
```
Analyze this E. coli RNA-seq dataset from a heat shock experiment. Identify differentially expressed genes, perform pathway enrichment analysis, and generate 2-3 testable hypotheses about the heat shock response mechanism. Create publication-quality visualizations (heatmap, volcano plot, pathway diagram).
```

**Use Edison API:**
- Job type: `JobNames.ANALYSIS`
- Data upload: `task3_ecoli_heatshock.csv`
- Expected runtime: ~45 minutes
- Cost: ~$200/run
- Language: Python (or R if preferred)

### 3. Parse Results

Extract from Kosmos output:
- **Differentially expressed genes (DEGs):** List with fold-changes
- **Generated hypotheses:** 2-3 testable statements
- **Analysis notebook:** Executable code
- **Figures:** Images (PNG/PDF)
- **Execution log:** stdout/stderr from code execution

Save to:
- `output/task3_results/kosmos_raw_output.json`
- `output/task3_results/analysis_notebook.ipynb` (or .py)
- `output/task3_results/figures/*.png`

### 4. Compare to Ground Truth

**Ground Truth - Known E. coli heat shock response:**
```json
{
  "canonical_upregulated_genes": [
    "dnaK",  "dnaJ", "groEL", "groES", "htpG", "clpB", "ibpA", "ibpB",
    "rpoH",  "ftsJ", "hslU", "lon"
  ],
  "expected_pathways": [
    "protein folding",
    "chaperone-mediated protein folding",
    "response to heat",
    "proteolysis"
  ],
  "known_mechanisms": [
    "sigma-32 (rpoH) regulon activation",
    "DnaK-DnaJ-GrpE chaperone system",
    "GroEL-GroES chaperonin complex",
    "Lon and Clp protease activation"
  ]
}
```

Save to: `input/task3_ground_truth.json`

### 5. Calculate Metrics

Run automated evaluation:

```python
# File: src/task3_evaluate.py

def calculate_gene_recall(identified_degs, ground_truth):
    """% of canonical heat shock genes identified as DEGs"""
    identified_set = set([g.lower() for g in identified_degs])
    canonical_set = set([g.lower() for g in ground_truth["canonical_upregulated_genes"]])
    overlap = identified_set & canonical_set
    recall = len(overlap) / len(canonical_set)
    return recall, list(overlap)

def test_notebook_execution(notebook_path):
    """Can the generated notebook execute without errors?"""
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor

    try:
        with open(notebook_path) as f:
            nb = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(timeout=600)
        ep.preprocess(nb, {'metadata': {'path': './'}})
        return True, None
    except Exception as e:
        return False, str(e)

def count_figures(output_dir):
    """Count generated figures"""
    import os
    fig_dir = os.path.join(output_dir, "figures")
    if not os.path.exists(fig_dir):
        return 0
    return len([f for f in os.listdir(fig_dir) if f.endswith(('.png', '.pdf', '.jpg'))])

def evaluate_hypotheses(hypotheses, ground_truth_mechanisms):
    """Qualitative: Do hypotheses relate to known mechanisms?"""
    # Simple keyword matching
    score = 0
    for hyp in hypotheses:
        hyp_lower = hyp.lower()
        for mechanism in ground_truth_mechanisms:
            if any(word in hyp_lower for word in mechanism.lower().split()):
                score += 1
                break
    return score / len(hypotheses) if hypotheses else 0
```

**Metrics to calculate:**
- **Gene recall:** % of `canonical_upregulated_genes` identified (target: ≥66%, i.e., 4/6 core genes)
- **Code execution:** Notebook runs without errors (target: True)
- **Figure count:** Number of generated visualizations (target: ≥2)
- **Hypothesis quality:** Overlap with known mechanisms (target: ≥50%)

Save to: `output/task3_results/metrics.json`

### 6. Generate Report

Create: `output/task3_results/task3_report.md`

**Template:**
```markdown
# Task 3: Systems Biology - Results

## Execution Summary
- **Start time:** {timestamp}
- **End time:** {timestamp}
- **Duration:** {minutes}
- **Cost:** $200

## Kosmos Query
{query text}

## Dataset
- **Source:** {GEO ID or simulated}
- **Dimensions:** {N genes × M samples}
- **Conditions:** {control vs. heat shock}

## Ground Truth Comparison

### Differentially Expressed Genes (DEGs)
| Gene | Fold-Change (Kosmos) | In Canonical Set | Known Function |
|------|---------------------|------------------|----------------|
| dnaK | {FC} | ✓ | Hsp70 chaperone |
| dnaJ | {FC} | ✓ | Hsp40 co-chaperone |
| groEL | {FC} | ✓ | Hsp60 chaperonin |
| groES | {FC} | ✓ | Hsp10 co-chaperonin |
| htpG | {FC} | ✓ | Hsp90 |
| clpB | {FC} | ✓ | Disaggregase |
| ... | ... | ... | ... |

**Gene Recall:** {X}% ({Y}/{Z} canonical genes found)

**Genes Identified:** {N total DEGs}
**Canonical genes in top 50:** {M}

### Generated Hypotheses
1. {Hypothesis 1}
   - Relates to known mechanism: ✓/✗ ({which one})

2. {Hypothesis 2}
   - Relates to known mechanism: ✓/✗

3. {Hypothesis 3}
   - Relates to known mechanism: ✓/✗

**Hypothesis quality score:** {X}%

### Code Execution
- **Notebook path:** `analysis_notebook.ipynb`
- **Executed successfully:** ✓/✗
- **Execution time:** {seconds}
- **Errors:** {list any errors or "None"}

### Figures Generated
- **Count:** {N} (target: ≥2)
- **Types:**
  - [ ] Heatmap
  - [ ] Volcano plot
  - [ ] Pathway diagram
  - [ ] Other: {describe}

**Sample figure:**
![Heatmap](figures/heatmap.png)

## Metrics

| Metric | Target | Actual | Pass/Fail |
|--------|--------|--------|-----------|
| Gene recall | ≥66% | {X}% | PASS/FAIL |
| Code execution | True | {T/F} | PASS/FAIL |
| Figure count | ≥2 | {N} | PASS/FAIL |
| Hypothesis quality | ≥50% | {Y}% | PASS/FAIL |

## Overall Assessment
**PASS/FAIL:** {based on ≥3/4 metrics passing}

## Qualitative Observations
{Notes on:
- Code quality (readable, well-commented?)
- Statistical rigor (p-values, FDR correction?)
- Biological insight (hypotheses testable and non-obvious?)
- Figure quality (publication-ready?)
}

## Raw Outputs
- Kosmos response: `kosmos_raw_output.json`
- Analysis notebook: `analysis_notebook.ipynb`
- Figures: `figures/*.png`
- Metrics: `metrics.json`
- Execution log: `../logs/task3_execution.log`

## Notes
{Any issues with data format, API, execution time}
```

## File Naming Convention
- Source code: `src/task3_*.py`
- Input data: `input/task3_ecoli_heatshock.csv`, `input/task3_ground_truth.json`
- Outputs: `output/task3_results/*`
- Logs: `logs/task3_execution.log`

## Success Criteria
- [ ] Kosmos job completes successfully
- [ ] Analysis notebook saved and executable
- [ ] ≥2 figures generated
- [ ] All 4 metrics calculated
- [ ] Report generated
- [ ] ≥3/4 metrics pass targets

## If Job Fails
1. Save error message to `logs/task3_error.log`
2. Check if partial results available (e.g., notebook with errors)
3. Document failure mode in report
4. Mark overall assessment as FAIL

## Tools Available
- Edison Python SDK
- nbformat, nbconvert (for notebook execution)
- pandas, numpy (for data handling)
- Pillow (for image verification)
- pytest

## Budget
$200 for this experiment (1 Kosmos ANALYSIS run)

## Timeline
Target completion: 60 minutes (45 min Kosmos + 15 min evaluation)

## Additional Notes
- This is the longest-running experiment (~45 min)
- Code quality is important but secondary to correctness
- Hypotheses should be testable (e.g., "dnaK overexpression will improve thermotolerance")
- Figures should be labeled with axes, legends, titles
