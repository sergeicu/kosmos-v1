# PRD: Kosmos RCT Pilot Testing System

## Executive Summary
Build automated testing system to validate Kosmos's utility for computational biology research proposal generation across 5 domains in a 2-hour pilot, using TDD methodology and parallel execution.

## Goals
1. **Validate tool efficacy:** Quantify Kosmos performance against ground truth benchmarks
2. **Identify optimal use cases:** Determine which job types provide most value for proposal generation
3. **De-risk full RCT:** Test methodology before deploying to 10-15 participants

## Non-Goals
- Full proposal generation (scope: proposal-relevant subtasks only)
- Long-term productivity tracking (scope: single 2-hour session)
- Tool comparison (scope: Kosmos only, not vs. competitors)

---

## Success Metrics

### Quantitative (Automated)
| Metric | Target | Measurement |
|--------|--------|-------------|
| **Citation accuracy** | 100% spot-check valid | Random sample 5 citations/experiment, verify existence |
| **Execution success** | ≥80% experiments complete | 4/5 experiments finish without fatal errors |
| **Code execution** | 100% notebooks run | Analysis job generates executable code |
| **Ground truth recall** | ≥75% known items found | % of known targets/trials/genes identified |

### Qualitative (Manual Expert Review)
| Dimension | Target | Scale |
|-----------|--------|-------|
| **Proposal relevance** | ≥4/5 | Likert 1-5: Would this strengthen a grant? |
| **Actionability** | ≥4/5 | Likert 1-5: Can researcher use immediately? |
| **Novelty detection** | ≥4/5 | Precedent job accurately identifies research gaps |

### Cost/Time
- **Budget:** $1000 (5 experiments × $200/run)
- **Time:** ≤2 hours total execution
- **Setup:** ≤1 hour (API setup, dataset preparation)

---

## Technical Architecture

### Folder Structure
```
kosmos/
├── brainstorm/
│   ├── brainstorm_user_needs.md
│   ├── brainstorm_tools.md
│   └── brainstorm_tests.md
├── tasks/
│   ├── overview/
│   │   ├── prd.md (this file)
│   │   └── plan_phase1.md
│   ├── s20251206_phase0_api_test/
│   │   ├── src/phase0_test_api.py
│   │   ├── input/ (empty)
│   │   ├── output/phase0_results/
│   │   └── logs/phase0_execution.log
│   ├── s20251206_phase1_smoke_tests/
│   │   ├── src/phase1_test_jobs.py
│   │   ├── input/ (empty)
│   │   ├── output/phase1_results/
│   │   └── logs/phase1_execution.log
│   ├── s20251206_task1_cancer_genomics/
│   │   ├── src/task1_literature.py
│   │   ├── input/task1_ground_truth.json
│   │   ├── output/task1_results/
│   │   └── logs/task1_execution.log
│   ├── s20251206_task2_immunology/
│   ├── s20251206_task3_systems_bio/
│   ├── s20251206_task4_structural_bio/
│   └── s20251206_task5_neuroscience/
└── init_prompt/
    └── kosmos_v1.md
```

### Naming Convention
- **Tasks:** `s{YYYYMMDD}_task{N}_{domain_name}/`
- **Source files:** `task{N}_{job_type}.py`
- **Outputs:** `task{N}_results/`
- **Logs:** `task{N}_execution.log`

### Parallel Execution Model
1. **5 separate Claude Code instances**
2. **Each receives:** Task prompt markdown file
3. **Each executes:** Query → Kosmos → Parse → Evaluate → Report
4. **Each outputs:** Structured JSON + Markdown report
5. **Aggregation:** Single summary dashboard across all 5

---

## Experiment Design

### Experiment 1: Cancer Genomics
- **Job Type:** LITERATURE
- **Query:** "What are the most promising targetable dependencies in KRAS-mutant pancreatic cancer identified in the last 3 years, and what mechanisms underlie resistance to current targeted therapies?"
- **Ground Truth:** SHP2, SOS1, MRTX1133, MRTX849; MEK reactivation resistance
- **Metrics:** Target recall, citation count (≥20), citation validity (100%)
- **Time:** 15 min

### Experiment 2: Immunology
- **Job Type:** PRECEDENT
- **Query:** "Has anyone developed mRNA vaccines targeting solid tumor neoantigens using patient-specific mutation profiles, and what were the clinical trial outcomes?"
- **Ground Truth:** NCT02410733, NCT03313778, NCT03639714
- **Metrics:** Trial recall (≥2/3), precedent accuracy (binary), outcome completeness
- **Time:** 15 min

### Experiment 3: Systems Biology
- **Job Type:** ANALYSIS
- **Query:** Analyze E. coli heat shock RNA-seq dataset
- **Ground Truth:** dnaK, dnaJ, groEL, groES, htpG, clpB upregulation
- **Metrics:** Gene recall (≥4/6), code execution success, figure generation (≥2)
- **Time:** 45 min

### Experiment 4: Structural Biology
- **Job Type:** MOLECULES
- **Query:** "Design three small molecule inhibitors for SARS-CoV-2 Mpro with improved oral bioavailability compared to nirmatrelvir. Provide ADMET predictions and synthetic accessibility scores."
- **Ground Truth:** Nirmatrelvir baseline properties
- **Metrics:** Chemical validity (3/3 valid SMILES), ADMET completeness, property improvement (≥1/3)
- **Time:** 30 min

### Experiment 5: Neuroscience
- **Job Type:** LITERATURE
- **Query:** "What circuit-level mechanisms link gut microbiome dysbiosis to Parkinson's disease pathology, and which are most amenable to therapeutic intervention?"
- **Ground Truth:** α-synuclein, vagus nerve, LPS, neuroinflammation
- **Metrics:** Mechanism recall (≥3/4), intervention ranking present, primary citations (≥15)
- **Time:** 15 min

---

## Implementation Phases

### Phase 0: API Connectivity (TDD)
**Objective:** Validate Edison API access works

**Tests (write first):**
1. `test_import_edison_client()`
2. `test_authenticate()`
3. `test_basic_query()`

**Implementation:** Minimal code to pass tests

**Verification:** All tests green

### Phase 1: Job Type Smoke Tests (TDD)
**Objective:** Confirm each job type can be invoked

**Tests (write first):**
1. `test_literature_job_callable()`
2. `test_analysis_job_callable()`
3. `test_precedent_job_callable()`
4. `test_molecules_job_callable()`

**Implementation:** Job submission code

**Verification:** All tests green (jobs may fail, but must be callable)

### Phase 2: Benchmark Experiments
**Objective:** Run 5 experiments with ground truth evaluation

**Process per experiment:**
1. Prepare input data
2. Submit Kosmos job
3. Parse results
4. Compare to ground truth
5. Generate report

**Parallelization:** 5 Claude Code instances simultaneously

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| API rate limits | Medium | High | Sequential fallback if parallel fails |
| Dataset incompatibility | Medium | Medium | 2 backup datasets per experiment |
| Citation fabrication | Low | Critical | 100% spot-check validation |
| Cost overrun | Low | Medium | Hard stop at $1000 budget |
| Execution timeout | Medium | Medium | 2-hour hard deadline, skip low-priority tests |

---

## Deliverables

### 1. Technical Outputs
- [ ] Phase 0 test suite + passing implementation
- [ ] Phase 1 test suite + passing implementation
- [ ] 5 experiment results (JSON + Markdown)
- [ ] Aggregated metrics dashboard

### 2. Reports
- [ ] Per-experiment report (5 total)
  - Ground truth vs. actual comparison
  - Metrics table
  - Raw Kosmos output
  - Pass/fail assertions
- [ ] Executive summary
  - Overall success rate
  - Cost breakdown
  - Recommendations for full RCT

### 3. Code Artifacts
- [ ] Reusable test harness
- [ ] Ground truth datasets
- [ ] Evaluation scripts
- [ ] Parallel execution templates

---

## Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Setup** | 30 min | API keys, datasets, folder structure |
| **Phase 0** | 30 min | API connectivity tests passing |
| **Phase 1** | 30 min | Job type smoke tests passing |
| **Phase 2** | 2 hours | 5 experiments complete |
| **Review** | 30 min | Expert evaluation + report generation |
| **Total** | 4 hours | Full pilot complete |

---

## Open Questions
1. **Edison SDK documentation:** Where is Python client documented?
2. **Dataset access:** Which public datasets best match ground truth requirements?
3. **Expert reviewers:** Who can provide qualitative evaluation?
4. **Precedent scope:** Does it search beyond ClinicalTrials.gov?

---

## Approval Checklist
- [ ] API access confirmed
- [ ] Ground truth datasets identified
- [ ] Expert reviewers recruited
- [ ] Timeline feasible (4 hours total)
