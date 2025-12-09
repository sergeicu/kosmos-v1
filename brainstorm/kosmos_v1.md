# Kosmos 2-Hour Pilot Test - PRD

## Objective
Validate Kosmos's utility for research proposal generation across computational biology domains within a 2-hour time constraint.

## Test Design: Five Queries, Four Job Types

**Total Time:** 2 hours
**Approach:** Pre-formulated queries testing each Kosmos capability across distinct comp bio domains
**Evaluation:** Speed, accuracy, citation quality, actionability for proposal writing

---

## Test Matrix

### 1. Cancer Genomics - LITERATURE (15 min)
**Query:** "What are the most promising targetable dependencies in KRAS-mutant pancreatic cancer identified in the last 3 years, and what mechanisms underlie resistance to current targeted therapies?"

**Rationale:** Tests literature synthesis for grant background sections
**Success Metric:** Comprehensive cited summary with ≥20 primary sources, identifies 3+ novel targets

---

### 2. Immunology/Vaccine Development - PRECEDENT (15 min)
**Query:** "Has anyone developed mRNA vaccines targeting solid tumor neoantigens using patient-specific mutation profiles, and what were the clinical trial outcomes?"

**Rationale:** Tests novelty assessment critical for proposal justification
**Success Metric:** Clear yes/no with clinical trial IDs, identifies research gaps

---

### 3. Systems Biology - ANALYSIS (45 min)
**Query:** Analyze multi-omics dataset (transcriptomics + metabolomics) from time-course bacterial stress response

**Data:** Mock or public dataset (e.g., E. coli heat shock, ~500 genes, 6 timepoints)
**Rationale:** Tests data-driven hypothesis generation for proposal methods
**Success Metric:** Executable analysis notebook, identifies 2+ testable hypotheses, generates publication-quality figures

---

### 4. Structural Biology - MOLECULES (30 min)
**Query:** "Design three small molecule inhibitors for the SARS-CoV-2 main protease (Mpro) with improved oral bioavailability compared to nirmatrelvir. Provide ADMET predictions and synthetic accessibility scores."

**Rationale:** Tests computational chemistry for drug discovery proposals
**Success Metric:** Three novel SMILES structures, documented property improvements, retrosynthesis routes

---

### 5. Neuroscience - LITERATURE (15 min)
**Query:** "What circuit-level mechanisms link gut microbiome dysbiosis to Parkinson's disease pathology, and which are most amenable to therapeutic intervention?"

**Rationale:** Tests cross-domain synthesis (microbiology + neuroscience)
**Success Metric:** Mechanistic pathways cited from primary literature, ranks intervention feasibility

---

## Evaluation Framework

### Quantitative Metrics (Per Query)
- **Execution Time:** Actual vs. estimated
- **Citation Count:** Number of primary sources
- **Citation Accuracy:** Spot-check 5 random citations (exist? relevant?)
- **Code Quality:** (ANALYSIS only) Runs without errors, generates outputs

### Qualitative Metrics (Expert Review)
- **Proposal Relevance:** Would output directly strengthen a grant application? (1-5 scale)
- **Novelty Detection:** Correctly identifies research gaps? (PRECEDENT)
- **Hypothesis Quality:** Are generated hypotheses testable and non-obvious? (ANALYSIS)
- **Actionability:** Can researcher immediately use output? (1-5 scale)

---

## Success Criteria

**Minimum Viable:**
- 4/5 queries complete within time budget
- ≥3/5 queries rated ≥4 on proposal relevance
- Zero fabricated citations in spot-checks
- ANALYSIS produces executable notebook

**Ideal:**
- All queries complete with time remaining
- All queries rated ≥4 on proposal relevance and actionability
- ANALYSIS identifies novel, literature-supported hypotheses
- MOLECULES designs chemically feasible compounds
- Outputs directly usable in mock proposal (qualitative assessment)

---

## Implementation Plan

### Pre-Test (15 min)
1. Identify public datasets for ANALYSIS query (E. coli Gene Expression Omnibus)
2. Prepare evaluation rubric spreadsheet
3. Recruit 1 comp bio expert for post-test qualitative review

### Execution (2 hours)
- Run queries sequentially (don't parallelize due to platform rate limits)
- Record start/end timestamps per query
- Save all outputs (notebooks, citations, molecular structures)

### Post-Test (30 min)
1. Citation spot-checking (5 per LITERATURE query)
2. Expert review of outputs
3. Compile quantitative metrics
4. Document failure modes and edge cases

---

## Risk Mitigation

**Risk:** ANALYSIS dataset incompatibility
**Mitigation:** Have 2 backup datasets pre-loaded (yeast osmotic stress, human PBMC scRNA-seq)

**Risk:** Queries timeout or fail
**Mitigation:** Pre-validate query syntax against Kosmos guidelines, have simplified fallback queries

**Risk:** Output quality too variable for conclusions
**Mitigation:** Focus on process metrics (speed, citation count) as secondary outcome if quality inconsistent

---

## Deliverables

1. **Metrics Report:** Execution times, citation counts, success rates per job type
2. **Expert Evaluation:** Qualitative assessment of 5 outputs
3. **Sample Outputs:** Best example from each job type for grant reporting
4. **Failure Analysis:** Documented edge cases where Kosmos underperformed
5. **Recommendation:** Which job types most valuable for proposal generation phase

---

## Next Steps Post-Pilot

If successful (≥3/5 meet success criteria):
- Scale to 10-15 participants with own research topics
- Measure time savings vs. manual literature review/analysis
- A/B test with/without Kosmos for matched proposal quality

If unsuccessful:
- Refine query formulation based on failure modes
- Focus on highest-performing job type only
- Consider alternative AI tools for comparison
