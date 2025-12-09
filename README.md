# Kosmos RCT Pilot Testing System

**Grant:** Schmidt Sciences
**Objective:** Validate Kosmos for computational biology research proposal generation
**Timeline:** 2-hour pilot across 5 experiments
**Budget:** $1000 (5 × $200/run)

---

## Quick Start

### Step 0: Critical Review (RECOMMENDED)
Run adversarial review BEFORE execution to identify flaws:
```bash
claude-code "Follow the instructions in tasks/task0_critical_review.md"
```

**Output:** 11 `_criticism.md` files + summary with GO/NO-GO recommendation

---

### For Sequential Execution (TDD)
```bash
# Phase 0: API connectivity (write tests first!)
claude-code "Follow the instructions in tasks/task_phase0_api_test.md"

# Phase 1: Job type smoke tests (write tests first!)
claude-code "Follow the instructions in tasks/task_phase1_smoke_tests.md"

# Phase 2: Run experiments sequentially
python tasks/s20251206_task1_cancer_genomics/src/task1_main.py
python tasks/s20251206_task2_immunology/src/task2_main.py
# ... etc
```

### For Parallel Execution (5 Claude Code Instances)
```bash
# Terminal 1
cd tasks/s20251206_task1_cancer_genomics && claude-code "Follow the instructions in ../task1_cancer_genomics.md"

# Terminal 2
cd tasks/s20251206_task2_immunology && claude-code "Follow the instructions in ../task2_immunology.md"

# Terminal 3
cd tasks/s20251206_task3_systems_bio && claude-code "Follow the instructions in ../task3_systems_bio.md"

# Terminal 4
cd tasks/s20251206_task4_structural_bio && claude-code "Follow the instructions in ../task4_structural_bio.md"

# Terminal 5
cd tasks/s20251206_task5_neuroscience && claude-code "Follow the instructions in ../task5_neuroscience.md"
```

---

## Experiments Overview

| # | Domain | Job Type | Query Focus | Time | Ground Truth |
|---|--------|----------|-------------|------|--------------|
| **0** | **Red Team** | **Review** | **Adversarial critique of plan** | **2-3h** | **Scientific/engineering best practices** |
| 1 | Cancer genomics | LITERATURE | KRAS-mutant PDAC targets | 15m | SHP2, SOS1, MRTX1133 |
| 2 | Immunology | PRECEDENT | mRNA neoantigen vaccines | 15m | NCT02410733, NCT03313778, NCT03639714 |
| 3 | Systems biology | ANALYSIS | E. coli heat shock RNA-seq | 45m | dnaK, groEL, clpB upregulation |
| 4 | Structural biology | MOLECULES | Mpro inhibitor design | 30m | Nirmatrelvir baseline properties |
| 5 | Neuroscience | LITERATURE | Gut-brain axis in PD | 15m | α-synuclein, vagus nerve, LPS |

**Total execution time:** 2 hours (experiments only)
**Total with review:** 4-5 hours

---

## Success Criteria

### Per-Experiment Metrics

**Automated:**
- Citation accuracy: 100% spot-check valid (5 random)
- Execution success: Job completes without fatal errors
- Ground truth recall: ≥75% known items identified

**Manual:**
- Proposal relevance: ≥4/5 (expert review)
- Actionability: ≥4/5

### Overall Pilot Success
- **Minimum:** 4/5 experiments complete, ≥3/5 pass metrics, zero fabricated citations
- **Ideal:** All 5 complete, all pass metrics, expert rating ≥4/5

---

## Phased Implementation (TDD)

### Phase 0: API Connectivity (30 min)
Tests → Implementation → All green

### Phase 1: Job Type Smoke Tests (30 min)
Tests → Implementation → All green

### Phase 2: Benchmark Experiments (2 hours)
Parallel execution via 5 Claude Code instances

---

## File Structure

```
tasks/
├── overview/
│   ├── prd.md                    # Product requirements
│   └── plan_phase1.md            # Implementation plan
├── task1_cancer_genomics.md      # Standalone prompt
├── task2_immunology.md
├── task3_systems_bio.md
├── task4_structural_bio.md
├── task5_neuroscience.md
├── s20251206_phase0_api_test/
│   ├── src/phase0_*.py
│   ├── output/
│   └── logs/
├── s20251206_task1_cancer_genomics/
│   ├── src/task1_*.py
│   ├── input/task1_ground_truth.json
│   ├── output/task1_results/
│   │   ├── kosmos_raw_output.json
│   │   ├── metrics.json
│   │   └── task1_report.md
│   └── logs/task1_execution.log
└── ... (tasks 2-5 similar structure)
```

---

## Environment Setup

```bash
pip install edison-client pytest requests pandas numpy scipy rdkit nbformat nbconvert
export EDISON_API_KEY="your_key_here"
```

---

## Next Steps

1. Obtain Edison API key
2. Run Phase 0/1 tests
3. Launch 5 parallel experiments
4. Aggregate results

---

## References

- [Kosmos Guidelines](https://edisonscientific.gitbook.io/edison-cookbook/edison-client/docs/kosmos_guidelines)
- [Analysis Tutorial](https://edisonscientific.gitbook.io/edison-cookbook/edison-client/docs/edison_analysis_tutorial)
- [Phoenix/Molecules](https://edisonscientific.gitbook.io/edison-cookbook/edison-client/docs/phoenix_guidelines)
