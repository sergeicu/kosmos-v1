# Edison / Kosmos Pilot Test

**Date:** December 9, 2025

---

## Executive Summary

Designed and executed a testing framework across five computational biology domains, with automated metrics for evaluating Edison generated content accuracy and utility.

**Current Status:** All 28 experiments completed, with the pilot study's 5 core experiments finished. Success rate: 22/28 successful, 5 failed, 1 pending when writing.

**Overall Pilot Results:**
- Tasks 3 & 4 (EDISON TOOLS: ANALYSIS & MOLECULES): ✅ Perfect scores
- Tasks 1, 2, 5 (EDISONS TOOLS: LITERATURE & PRECEDENT): Mixed results with valuable insights
- All technical challenges had been overcome with workarounds

---

## 1. Why This Evaluation is Essential

### 1.1. First Impressions: Beyond the Hype

Through my own direct early direct testing of the Edison tools (via their UI interface) in my own field (medical AI research), I observed that Edison tools perform remarkably well. The system demonstrates:

- Ability to query, analyze, and synthesize complex scientific literature
- Executes Python notebook experiments with good technical accuracy
- Seamlessly connect between literature review and data analysis

The execution patterns strongly resemble the Claude Code environment but with crucial advantage: built-in integrations with academic databases through MCP servers (arXiv, PubMed, Clinical Trials API, etc.).

It makes sense that Edison offers a packaged solution that performs what Claude Code can do in a "ready meal" format - with integration services and optimized prompts. Regarding Kris' suggestion on GPT-5 comparison - I already feel that Edison is distinctly much more advanced and better than GPT5 offers from the box, for scientists. 

In professional terms (for a journal paper) - I think the better comparison would be between:
1. Edison Scientific's tools 
vs 
2. Claude Code (Anthropic) or Codex CLI tool (OpenAI) - general coding tools 

The real question from a technical perspective is: how well would a dry (non-optimized) coding tool from Anthropic or OpenAI compare to Edison's specialized offering? This is an evaluation I plan to conduct myself anyway.

### 1.2. Personal Experience: From Skepticism to Systematic Testing

Having tried the Edison tool, I find it quite good. UI is not perfect but I can see the beginning of what it wants to do. However, as someone with experience using Claude Code, I recognized the similarities immediately. This led to my next step: establish a swarm of parallel claude code agents to investigate the baseline performance of Edison.

My approach was to synthetically generate 5 tasks that are relevant to our grant (in comp bio) for which we derive KNOWN ground truth. The goal was to evaluate whether Edison could effectively recover the answers from literature - for things that are reliably well known in general sense. This would serve as my baseline test. If it can pass this, then I know I can trust it more.

### 1.3. The Trust Factor: Learning from OpenEvidence

This brings me to a crucial insight about trust. I remember using OpenEvidence extensively in its early days (another AI scientist tool focused on doctors, now the leading AI tool among physicians in the US - I and many others at Harvard Med love it!). Challgenge: in the early days of Open Evidence - I was verifying every result it gave me.

This verification step is key with these tools. It's something to consider deeply in our RCT design - the human verification component and how trust builds over time with continued accurate performance.


**Personal Note:** I truly believe that the UI quality and experience is crucial for Edison's future success. While Claude Code may have superior coding capabilities, having an interface that's easier to understand and poke around in will be key to making the scientific journey easier. At the moment I can see where the UI is going, but it is far far from perfect. Looking at a tool like Weights & Biases, or Open Evidence - the UI is much more intuitive and well laid out. In short - if i was Sam Rodrigues - i would throw ALL my effort in getting the UI to be workable.Right now it is 50% there. 

**Personal Note 2:** I personally noticed that Edison / Future House is trying to do EVERYTHING instead of one thing well. They have too many tools. While this may sound cool - it is actually at best very confusing - i am lost in the midst of the number of things they offer. E.g. Precedent, Analysis, Literature Search, Kosmos, Aviary - what isthe difference between all of these - i think it stops me more than it encourages me. 


### 1.4. The Implementation Gap: Why Packaged Solutions Matter 

While Claude Code is technically impressive and much more advanced, they present a significant barrier to entry for most scientists:

**Technical Expertise Required:**
- Understanding of agent orchestration and swarm management
- Experience with Claude Code and MCP server integration
- Knowledge of API workflows for multiple academic databases
- Software engineering skills for system maintenance

**Reality Check:**
Few scientists possess the combination of domain expertise AND technical skills needed to build such systems independently (Sundai coders is an exception even amongst the best MIT folks - i can give many stories on this from person experince). So - in a normal science setting - even those with some technical background would face substantial learning curves in:

1. Multi-agent system design
2. Database integration and authentication
3. Error handling and reliability engineering
4. Workflow optimization for research tasks

These are NOT the skills that a classic software engineer or scientific researcher possesses. These skills are the modern new skills that had just appeared on the horizon. This is why imho Edison is actually necessary. 

### 1.5. Study Design: Synthetic Ground Truth Approach

Being a scientist myself - still i want to verify if Edison works. For this - we design a verifiable experiment - 

Here's the setup i built - I created a swarm of parallel agents that investigated baseline performance of Edison. I synthetically generated 5 tasks spanning different computational biology domains, each with known ground truth. My goal was to evaluate whether the system could effectively recover known answers and establish a baseline level of trust in its capabilities. I.e. an attempt to establish a quantifiable evaluation framework. 


---

## 2. Study Design: A Rigorous Multi-Domain Approach

### 2.1. Overall Architecture

```
Edison / Kosmos Pilot Testing System
├── Phase 0: API Connectivity (TDD approach)
├── Phase 1: Job Type Validation (smoke tests)
└── Phase 2: Domain Experiments (5 parallel tracks)
    ├── Task 1: Cancer Genomics (Literature synthesis)
    ├── Task 2: Immunology (Precedent search)
    ├── Task 3: Systems Biology (Data analysis)
    ├── Task 4: Structural Biology (Molecular design)
    └── Task 5: Neuroscience (Cross-domain synthesis)
```

### 2.2. Methodological Innovation: Test-Driven Development

**Why TDD for AI Evaluation?**
Traditional AI benchmarks often fail in real-world scenarios. I used Test-Driven Development (TDD) to ensure:

1. **Ground truth validation:** Every claim must be verifiable against known scientific facts
2. **Automated metrics:** Objective, reproducible evaluation criteria
3. **Failure documentation:** Clear understanding of where and why tools fail
4. **Incremental validation:** Build confidence step by step

**Implementation:**
- Write tests before running AI queries
- Tests fail initially (no AI response)
- Run AI tool
- Evaluate if tests pass
- Document all failures and partial successes

### 2.3. The Five Experiments: Strategic Domain Selection

Each experiment tests a core research task scientists perform when writing grants:

| Domain | Job Type | Research Task | Why It Matters |
|--------|----------|---------------|----------------|
| **Cancer Genomics** | LITERATURE | Synthesizing recent breakthroughs | Tests knowledge currency and accuracy |
| **Immunology** | PRECEDENT | Finding prior work | Tests novelty validation for grants |
| **Systems Biology** | ANALYSIS | Data-driven discovery | Tests computational capabilities |
| **Structural Biology** | MOLECULES | Drug design | Tests specialized domain knowledge |
| **Neuroscience** | LITERATURE | Cross-disciplinary synthesis | Tests knowledge integration |

---

## 3. Experiment Execution: What We Actually Did

### 3.1. Infrastructure Setup

**Technical Architecture:**
- **Parallel execution:** 5 independent Claude Code instances
- **Time boxing:** 2-hour hard deadline
- **Automated logging:** Comprehensive audit trails

**File Organization:**
```

each_task/ (individual experiment specs)
├── input/ (ground truth data)
├── src/ (implementation code)
├── output/ (results and reports)
└── logs/ (execution traces)
```

### 3.2. Phase 0: API Connectivity Validation

**Objective:** Ensure basic access to Edison's API works before expensive experiments.

**Tests Written:**
1. `test_import_edison_client()`: Can we import the SDK?
2. `test_authenticate()`: Do API keys work?
3. `test_basic_query()`: Can we make a simple call?

**Outcome:** All tests passed, providing confidence for main experiments.

### 3.3. Phase 1: Job Type Validation

**Objective:** Confirm each Edison job type  works (LITERATURE, ANALYSIS, etc.).

**Key Insight:** This phase revealed that while API access works, job submission requires specific formatting and error handling. More can be read [here](https://github.com/sergeicu/kosmos-v1/blob/main/tasks/task_phase1_smoke_tests.md). 

### 3.4. Phase 2: The Main Experiments

#### **Experiment 1: Cancer Genomics (LITERATURE)**
- **Query:** KRAS-mutant pancreatic cancer targets and resistance mechanisms
- **Ground Truth:** Known targets (SHP2, SOS1, MRTX compounds) and resistance pathways
- **Status:** Successfully submitted (Task ID: 561fb2fd-06c8-4a17-9ce8-9e4020f09aa0)

#### **Experiment 2: Immunology (PRECEDENT)**
- **Query:** mRNA neoantigen vaccines in solid tumors
- **Ground Truth:** Clinical trials NCT02410733, NCT03313778, NCT03639714
- **Tests:** Trial identification accuracy, outcome reporting completeness

#### **Experiment 3: Systems Biology (ANALYSIS)**
- **Query:** E. coli heat shock RNA-seq analysis
- **Ground Truth:** Canonical heat shock genes (dnaK, groEL, etc.)
- **Unique Feature:** Tests actual code generation and data analysis

#### **Experiment 4: Structural Biology (MOLECULES)**
- **Query:** Design improved SARS-CoV-2 Mpro inhibitors
- **Ground Truth:** Nirmatrelvir properties as baseline
- **Innovation:** Automated SMILES validation using RDKit

#### **Experiment 5: Neuroscience (LITERATURE)**
- **Query:** Gut-brain axis in Parkinson's disease
- **Ground Truth:** Known mechanisms (α-synuclein, LPS, SCFAs)
- **Challenge:** Cross-domain synthesis tests

---

## 4. Evaluation Framework

### 4.1. Automated Metrics

Each experiment has domain-specific metrics:

| Experiment | Metric 1 | Metric 2 | Metric 3 | Metric 4 |
|------------|----------|----------|----------|----------|
| Cancer Genomics | Target recall (≥75%) | Citation validity (100%) | Citation count (≥20) | Key paper coverage |
| Immunology | Trial recall (≥66%) | Precedent accuracy (100%) | Outcome completeness | Paper coverage |
| Systems Biology | Gene recall (≥66%) | Code execution (True) | Figure count (≥2) | Hypothesis quality |
| Structural Biology | Chemical validity (100%) | ADMET completeness | Property improvement | Synthesis routes |
| Neuroscience | Mechanism recall (≥75%) | Ranking quality (τ≥0.5) | Citation count (≥15) | Primary research ratio |

### 4.2. Qualitative Evaluation

Beyond numbers, we assessed:
- **Proposal relevance:** Would this strengthen a grant application? (1-5 Likert)
- **Actionability:** Can a scientist use this immediately? (1-5 Likert)
- **Novelty detection:** Does the tool identify research gaps correctly?

### 4.3. Citation Validation

**Critical Innovation:** Automated spot-checking of citations via CrossRef API
```python
def verify_doi_exists(doi):
    response = requests.get(f"https://api.crossref.org/works/{doi}")
    return response.status_code == 200
```
This prevents AI hallucination from polluting scientific literature.

---

## 5. Experimental Results: All Five Domains Complete

The pilot study has completed with all five experiments successfully executed and evaluated. The results revealed strengths and areas for improvement:

**Success Summary:**
- ✅ **ANALYSIS (Systems Biology):** High performance in RNA-seq analysis
- ✅ **MOLECULES (Structural Biology):** Strong computational drug design
- ⚠️ **LITERATURE (Cancer Genomics):** Good synthesis, citation issues
- ⚠️ **PRECEDENT (Immunology):** Correct answers, trial identification challenges
- ⚠️ **LITERATURE (Neuroscience):** Strong synthesis, terminology mismatch

Below are detailed findings from each domain:

### 5.1. Task 1: Cancer Genomics (LITERATURE)
**[📊 View Executive Report](https://github.com/sergeicu/kosmos-v1/blob/main/output/task1_results/task1_report_executive.md)** |
**[🔗 View Edison Platform](https://platform.edisonscientific.com/trajectories/561fb2fd-06c8-4a17-9ce8-9e4020f09aa0)**

**Key Results:**
- Status: ❌ FAIL overall (3/4 metrics failed)
- Target Recall: 60% (found 3/5 known targets: MRTX1133, SHP2, SOS1)
- Citation Count: Only 6 citations (target: ≥20)
- **Success:** 100% citation validity, perfect resistance mechanism coverage
- **Missed:** MRTX849 (FDA-approved), key 2023 Nature papers

**What Edison Found:**
- Identified daraxonrasib (RMC-6236) - novel pan-RAS inhibitor
- Provided 12 active NCT trial IDs
- Comprehensive resistance mechanism synthesis

**Technical Issues:**
- Provided clinical trial IDs instead of research paper DOIs
- Ground truth mismatch: focused on trials over foundational papers

### 5.2. Task 2: Immunology (PRECEDENT)
**[📊 View Executive Report](https://github.com/sergeicu/kosmos-v1/blob/main/output/task2_results/task2_report_executive.md)** |
**[🔗 View Edison Platform](https://platform.edisonscientific.com/trajectories/9e573c63-aa7d-4f79-adc3-501ffc4ba279)**

**Key Results:**
- Status: ❌ FAIL overall (2/4 metrics failed)
- Precedent Accuracy: ✅ 100% (correctly identified vaccines exist)
- NCT Trial Recall: ❌ 0% (didn't find specific trial IDs)
- Enhanced Recall: 33.3% (found mRNA-4157 but missed others)

**What Edison Found:**
- mRNA-4157 (Moderna) - Phase 2b data: improved RFS (HR 0.56)
- Autogene cevumeran (BioNTech) - Phase I: 50% T-cell response rate
- Detailed efficacy and safety outcomes

**Technical Issues Fixed:**
- API returns "success" not "completed" status
- Enhanced evaluation to recognize product names, not just NCT IDs

### 5.3. Task 3: Systems Biology (ANALYSIS)
**[📊 View Executive Report](https://github.com/sergeicu/kosmos-v1/blob/main/output/task3_results/task3_report_executive.md)** |
**[🔗 View Edison Platform](https://platform.edisonscientific.com/trajectories/86d6c8a2-9d7c-42d6-abc7-bd40f2d46474)**

**Key Results:**
- Status: ✅ PASS (all 4 metrics passed!)
- Gene Recall: 100% (all 8 canonical heat shock genes identified)
- Code Execution: ✅ Complete R/DESeq2 analysis notebook
- Figure Count: 3/3 (volcano plot, heatmap, bar plot)
- Hypothesis Quality: 100% (all 3 hypotheses biologically relevant)

**What Edison Found:**
- 13 significant DEGs (8 upregulated chaperones)
- Fold changes: dnaK (4.0x), groEL (5.9x), ibpB (4.9x)
- Three testable hypotheses about chaperone regulation

**Technical Issues Fixed:**
- File uploads fail with ANALYSIS jobs
- Implemented inline data workaround
- Successfully demonstrated full capability without uploads

### 5.4. Task 4: Structural Biology (MOLECULES)
**[📊 View Executive Report](https://github.com/sergeicu/kosmos-v1/blob/main/output/task4_results/task4_report_executive.md)** |
**[🔗 View Edison Platform](https://platform.edisonscientific.com/trajectories/46d09be4-cbe6-4138-837e-54766594fd4a)**

**Key Results:**
- Status: ✅ PASS (all 4 metrics passed!)
- Chemical Validity: 100% (all 3 molecules have valid SMILES)
- Property Improvement: 100% (all show ≥1 improved property)
- ADMET Completeness: 100%
- Synthesis Routes: 100% (all include retrosynthesis)

**What Edison Designed:**
- **Molecule 1:** 185,768 μg/mL solubility (vs 135 for nirmatrelvir)
- **Molecule 3:** 792,447 μg/mL solubility (dramatic improvement)
- All maintained reasonable bioavailability (32-47% vs 50% baseline)
- SAScores 4.45-4.53 (synthetically accessible)

**Technical Issues Fixed:**
- API uses "answer" field not "result" field
- Custom parser for molecular properties
- Converted logS to μg/mL for proper comparison

### 5.5. Task 5: Neuroscience (LITERATURE)
**[📊 View Executive Report](https://github.com/sergeicu/kosmos-v1/blob/main/output/task5_results/task5_report_executive.md)** |
**[🔗 View Edison Platform](https://platform.edisonscientific.com/trajectories/0ee36475-e575-4d67-9e14-dbdfd97103dd)**

**Key Results:**
- Status: ❌ FAIL overall (2/4 metrics failed)
- Mechanism Recall: 25% (1/4 established mechanisms)
- **Intervention Ranking:** ✅ Perfect (τ=1.00 correlation)
- Citation Count: 14 (just 1 short of target)
- Primary Research: 100% (all citations primary sources)

**What Edison Found:**
- LPS-induced neuroinflammation via TLR4/NF-κB pathway
- Perfect intervention feasibility ranking:
  1. Diet/pre/probiotics (RCTs available)
  2. SIBO/H. pylori management
  3. FMT (pilot studies)
  4. Vagal neuromodulation (exploratory)
- Excellent cross-domain synthesis quality

**Technical Issues:**
- Terminology differences from ground truth
- Fuzzy matching needed for equivalent mechanisms

### 5.6. Overall Pilot Assessment

**Success Rate:** 2/5 tasks passed all metrics (40%)

**Key Insights:**

**Strengths of Edison Tools:**
1. **Technical Capabilities:** High performance in ANALYSIS and MOLECULES tasks
   - Complete RNA-seq analysis with executable R/DESeq2 code (100% gene recall)
   - Chemically valid molecular structures with improved solubility profiles
   - Generation of biologically relevant, testable hypotheses

2. **Integration Value:** Demonstrated ability to combine multiple capabilities
   - Literature synthesis effectively linked to experimental design
   - Cross-domain knowledge integration (microbiology + neuroscience)
   - Clinical trial awareness and outcome reporting

3. **User Experience:** UI reduces complexity of scientific workflows
   - Lowers technical barriers for non-programmer scientists
   - Provides integrated scientific tools (vs. separate CLI tools)
   - Interactive visualizations and real-time feedback


---

## 6. Connection to Full RCT: Why This Eval Matters

### 6.1. De-risking the Main Study

This eval addresses critical risks before the mini 10-15 participant RCT:

1. **Technical risk:** ✓ API access works
2. **Evaluation risk:** ✓ Metrics framework validated
3. **Time risk:** ✓ 2-hour execution window feasible (if you know what you are doing)
4. **Relevance risk:** ✓ Tasks map well to real research needs

### 6.2. Scaling Considerations

**From Pilot (5 experiments) to mini RCT (10-15 scientists):**

| Aspect | Pilot | RCT Scale | Scaling Factor |
|--------|-------|-----------|----------------|
| Experiments | 5 | 50-75 | 10-15x |
| Evaluation | Automated | Mixed auto/manual | Added human review |
| Domains | 5 | 5 (consistent) | None |
| Duration | 4 hours | One day? | Extended timeline |

### 6.3. Key RCT Questions Informed by This Eval

**Question 1: Productivity Impact**
- Eval establishes baseline task completion times
- Provides metrics for productivity measurement

**Question 2: Quality Assessment**
- Eval shows AI can identify correct scientific concepts
- Reveals need for human expert validation (KEY)
- Demonstrates importance of citation verification

**Question 3: User Experience**
- Parallel execution model scales to multiple users -> but this is only for CLI based execution 
- Clear file organization prevents confusion
- Comprehensive logging supports research compliance

---


### 7. My Insights / Personal Thoughts 

**Demand Signals:**
- High need for literature synthesis tools with simple UI 
- Gap in data analysis automation (semi addressed by Edison)
- Critical need for validation and verification

**Competitive Landscape:**
- Edison vs. specialized tools (e.g., AlphaFold, ChemAxon) or general coding tools (Codex CLI/Claude Code) 
- Integration challenges across domains
- Opportunity in workflow orchestration

---

## 8. Recommendations For the Mini RCT 

1. **Clearly define eval BEFORE:** It is paramount to narrow dowh the topics, clearly define the metrics AHEAD of any hackathon 
2. **Add human experts:** We need domain scientists for qualitative review 

---

## 9. Conclusion

This eval demonstrates that rigorous evaluation of AI tools for scientific research is essential. For us to be able to CLEARLY evaluate performance we will need to define the eval metrics ahead of time and narrow them down succinctly. The initial hands-on experience with Edison showed impressive capabilities in medical AI research for me, but it was impossible to tell personally if it was good or bad (really i had no clue). This is why I decided to embark on the adventure of verifying what this system is capable of in a quantified and verifiable way. I think this is the most important task for us and for Edison/FH team altogether. 

More broadly, I think edison UI tools need much improvement to be not just attractive but actually useful to scientists. We would stuggle to recruit scientists at this moment to use it for a long time as some key UI components are mediocre. While GPT5 may be much less impressive, the familiarity with the tool still is superior reason why most scientists would use it over Edison imho. 


---

## Appendix: Technical Details

### A. Links to Full Executive Reports

1. **Task 1: Cancer Genomics**
   - [Executive Report](https://github.com/sergeicu/kosmos-v1/blob/main/output/task1_results/task1_report_executive.md)
   - [Edison Platform](https://platform.edisonscientific.com/trajectories/561fb2fd-06c8-4a17-9ce8-9e4020f09aa0)

2. **Task 2: Immunology**
   - [Executive Report](https://github.com/sergeicu/kosmos-v1/blob/main/output/task2_results/task2_report_executive.md)
   - [Edison Platform](https://platform.edisonscientific.com/trajectories/9e573c63-aa7d-4f79-adc3-501ffc4ba279)

3. **Task 3: Systems Biology**
   - [Executive Report](https://github.com/sergeicu/kosmos-v1/blob/main/output/task3_results/task3_report_executive.md)
   - [Edison Platform](https://platform.edisonscientific.com/trajectories/86d6c8a2-9d7c-42d6-abc7-bd40f2d46474)

4. **Task 4: Structural Biology**
   - [Executive Report](https://github.com/sergeicu/kosmos-v1/blob/main/output/task4_results/task4_report_executive.md)
   - [Edison Platform](https://platform.edisonscientific.com/trajectories/46d09be4-cbe6-4138-837e-54766594fd4a)

5. **Task 5: Neuroscience**
   - [Executive Report](https://github.com/sergeicu/kosmos-v1/blob/main/output/task5_results/task5_report_executive.md)
   - [Edison Platform](https://platform.edisonscientific.com/trajectories/0ee36475-e575-4d67-9e14-dbdfd97103dd)

### B. Evaluation Code Snippets

```python
# Citation validation
def validate_citations_sample(citations, n=5):
    sample = random.sample(citations, min(n, len(citations)))
    valid = sum(1 for c in sample if verify_doi_exists(c))
    return valid / len(sample)

# Chemical validity check
def validate_smiles(smiles_str):
    mol = Chem.MolFromSmiles(smiles_str)
    return mol is not None

# Ranking quality assessment
def evaluate_intervention_ranking(kosmos_ranking, expected_order):
    tau, _ = kendalltau(kosmos_ranking, expected_order)
    return tau
```



**Prepared by:**
Serge on Sunday 7 Dec 2025 as part of Sundai 
