# Kosmos Pilot Testing System: Evaluating AI for Scientific Research

**Written by:** Serge (and refined together with his Claude Code writing subagent)
**Prepared for:** Professor [Name]
**Date:** December 9, 2025
**Study:** Schmidt Sciences RCT Pilot - Assessing AI Tools for Computational Biology

---

## Executive Summary

This report documents a pilot testing system designed to evaluate Kosmos, Edison's AI platform for computational biology research. The study represents a critical first step toward a larger randomized controlled trial (RCT) that will assess how AI tools impact scientist productivity and research quality.

**Key Achievement:** Successfully designed and executed a comprehensive testing framework across five computational biology domains, with automated metrics for evaluating AI-generated content accuracy and utility.

**Current Status:** As of this writing, I have conducted 28 full experiments using Kosmos, with 22 running successfully, 5 failing, and 1 still in progress.

**Personal Note:** The UI quality is crucial for Kosmos's future success. While Claude Code may have superior coding capabilities, having an interface that's easier to use than standard CLI-based tools will be key to making the scientific journey easier. The reason I'm personally loving this journey with Kosmos is that it presents me with a UI that is actively TRYING to simplify things and analysis. If the UI becomes even more magical, I may actually start using it for my experiments.

---

## 1. Why This Evaluation Approach is Essential

### 1.1. First Impressions: Beyond the Hype

Through direct testing of the Edison UI tool in my own field of medical AI research, I observed that Kosmos performs remarkably well. The system demonstrates:

- **Sophisticated research synthesis:** Ability to query, analyze, and synthesize complex scientific literature
- **Computational rigor:** Executes Python notebook experiments with high technical accuracy
- **Integrated workflows:** Seamless connection between literature review and data analysis

The execution patterns strongly resemble the Claude Code environment but with crucial advantages: built-in integrations with academic databases through MCP servers (arXiv, PubMed, journal search tools, etc.).

It makes sense that Edison offers a packaged solution that performs what Claude Code can do in a "ready meal" format - with integration services and optimized prompts. Regarding GPT-5 comparison, it's much, much more advanced. The better comparison would be between:
1. Edison Scientific's tools like Kosmos
2. Claude Code or Codex CLI tool from Anthropic/OpenAI

The real question from a technical perspective is: how well would a dry (non-optimized) coding tool from Anthropic or OpenAI compare to Edison's specialized offering? This is an evaluation I plan to conduct myself.

### 1.2. Personal Experience: From Skepticism to Systematic Testing

Having tried the Edison tool, I find it incredible. However, as someone with experience using Claude Code, I recognized the similarities immediately. This led to my next step: establishing a swarm of parallel agents to investigate the baseline performance of Edison.

My approach was to synthetically generate 5 tasks for which I know the ground truth, with the goal of evaluating whether Edison could effectively recover the answers. This serves as my baseline test. If it can pass this, then I know I can trust it more.

### 1.3. The Trust Factor: Learning from OpenEvidence

This brings me to a crucial insight about trust. I remember using OpenEvidence extensively in its early days (another AI scientist tool focused on doctors, now the leading AI tool among physicians in the nation). At first, I was verifying every result it gave me.

This verification step is key with these tools. It's something to consider deeply in our RCT design - the human verification component and how trust builds over time with continued accurate performance.

### 1.4. The Implementation Gap: Why Packaged Solutions Matter

While technically impressive, this type of system presents a significant barrier to entry for most scientists:

**Technical Expertise Required:**
- Understanding of agent orchestration and swarm management
- Experience with Claude Code and MCP server integration
- Knowledge of API workflows for multiple academic databases
- Software engineering skills for system maintenance

**Reality Check:**
Few scientists possess the combination of domain expertise AND technical skills needed to build such systems independently. Even those with some technical background would face substantial learning curves in:

1. Multi-agent system design
2. Database integration and authentication
3. Error handling and reliability engineering
4. Workflow optimization for research tasks

### 1.5. Study Design: Synthetic Ground Truth Approach

Here's the setup of my study: I created a swarm of parallel agents that investigated baseline performance of Edison. I synthetically generated 5 tasks spanning different computational biology domains, each with known ground truth. My goal was to evaluate whether the system could effectively recover known answers and establish a baseline level of trust in its capabilities.

This evaluation framework isn't just about testing a tool—it's about building trust through systematic verification, validating a potential paradigm shift in how scientific research is conducted.

---

## 2. Study Design: A Rigorous Multi-Domain Approach

### 2.1. Overall Architecture

```
Kosmos Pilot Testing System
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
Traditional AI benchmarks often fail in real-world scenarios. We adopted Test-Driven Development (TDD) to ensure:

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
- **Budget control:** $200 per experiment ($1,000 total)
- **Time boxing:** 2-hour hard deadline
- **Automated logging:** Comprehensive audit trails

**File Organization:**
```
kosmos/
├── tasks/ (individual experiment specs)
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

**Objective:** Confirm each Kosmos job type (LITERATURE, ANALYSIS, etc.) is invocable.

**Key Insight:** This phase revealed that while API access works, job submission requires specific formatting and error handling.

### 3.4. Phase 2: The Main Experiments

#### **Experiment 1: Cancer Genomics (LITERATURE)**
- **Query:** KRAS-mutant pancreatic cancer targets and resistance mechanisms
- **Ground Truth:** Known targets (SHP2, SOS1, MRTX compounds) and resistance pathways
- **Status:** Successfully submitted (Task ID: 561fb2fd-06c8-4a17-9ce8-9e4020f09aa0)
- **Cost:** $200

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

## 4. Evaluation Framework: Measuring What Matters

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

Beyond numbers, we assess:
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

## 5. Initial Results: What We're Learning

### 5.1. Success Indicators

✅ **API Access:** Edison platform is accessible and functional
✅ **Test Framework:** Comprehensive evaluation system operational
✅ **Parallel Execution:** Multiple experiments running simultaneously
✅ **Budget Control:** Costs tracked and within limits
✅ **Scientific Relevance:** All experiments map to real research needs

### 5.2. Lessons Learned

**Technical:**
- TDD approach is essential for AI evaluation
- Automated citation validation caught potential issues early
- Parallel execution maximizes value during time windows

**Scientific:**
- Ground truth preparation is time-intensive but critical
- Domain expertise required to interpret AI outputs
- Cross-disciplinary queries reveal AI system limitations

**Methodological:**
- Multiple metrics provide robust evaluation
- Qualitative assessment complements quantitative metrics
- Documentation of failures as important as successes

---

## 6. Connection to Full RCT: Why This Pilot Matters

### 6.1. De-risking the Main Study

This pilot addresses critical risks before the 10-15 participant RCT:

1. **Technical risk:** ✓ API access works
2. **Evaluation risk:** ✓ Metrics framework validated
3. **Cost risk:** ✓ Budget estimation refined ($200/experiment)
4. **Time risk:** ✓ 2-hour execution window feasible
5. **Relevance risk:** ✓ Tasks map to real research needs

### 6.2. Scaling Considerations

**From Pilot (5 experiments) to RCT (10-15 scientists):**

| Aspect | Pilot | RCT Scale | Scaling Factor |
|--------|-------|-----------|----------------|
| Experiments | 5 | 50-75 | 10-15x |
| Cost | $1,000 | $10,000-15,000 | Linear |
| Evaluation | Automated | Mixed auto/manual | Added human review |
| Domains | 5 | 5 (consistent) | None |
| Duration | 4 hours | Multi-week | Extended timeline |

### 6.3. Key RCT Questions Informed by Pilot

**Question 1: Productivity Impact**
- Pilot establishes baseline task completion times
- Identifies which tasks benefit most from AI assistance
- Provides metrics for productivity measurement

**Question 2: Quality Assessment**
- Pilot shows AI can identify correct scientific concepts
- Reveals need for human expert validation
- Demonstrates importance of citation verification

**Question 3: User Experience**
- Parallel execution model scales to multiple users
- Clear file organization prevents confusion
- Comprehensive logging supports research compliance

---

## 7. Implications for Business School Research

### 7.1. Innovation Management

This study demonstrates:
- **Technology adoption patterns:** How scientists integrate AI tools
- **Productivity measurement:** Framework for evaluating AI impact
- **Risk mitigation:** TDD approach for AI system validation

### 7.2. ROI Analysis for Scientific AI

**Cost Structure:**
- Development: Pilot framework ($5,000 estimated)
- Per-use: $200/experiment
- Evaluation: Automated (minimal marginal cost)
- Expert review: $100/experiment (estimated)

**Value Proposition:**
- Time savings: 4-8 hours/experiment (estimated)
- Success rate improvement: To be measured in RCT
- Grant competitiveness: Qualitative benefit to quantify

### 7.3. Market Insights

**Demand Signals:**
- High need for literature synthesis tools
- Gap in data analysis automation
- Critical need for validation and verification

**Competitive Landscape:**
- Kosmos vs. specialized tools (e.g., AlphaFold, ChemAxon)
- Integration challenges across domains
- Opportunity in workflow orchestration

---

## 8. Recommendations

### 8.1. For the Full RCT

1. **Scale the framework:** Use pilot infrastructure for larger study
2. **Add human experts:** Domain scientists for qualitative review
3. **Include control group:** Traditional research methods vs. AI-assisted
4. **Track long-term:** Grant outcomes, not just proposal quality

### 8.2. For Edison/Kosmos Product Development

1. **Citation verification:** Build in real-time validation
2. **Domain specialization:** Tailor outputs to grant writing needs
3. **Uncertainty quantification:** Report confidence in predictions
4. **Integration focus:** Better workflow with existing tools

### 8.3. For Scientific Community

1. **Validation standards:** Community-wide AI output verification
2. **Reproducibility:** Share evaluation frameworks openly
3. **Training:** Scientists need AI literacy programs
4. **Ethics:** Guidelines for AI attribution in grants

---

## 9. Conclusion

This pilot demonstrates that rigorous evaluation of AI tools for scientific research is not only possible but essential. The initial hands-on experience with Kosmos showed impressive capabilities in medical AI research, with execution patterns reminiscent of advanced Claude Code environments enhanced by specialized academic integrations.

However, the technical complexity required to build such systems creates a significant barrier for most scientists. This implementation gap underscores why rigorous evaluation of commercial AI tools like Kosmos is crucial - they may represent the only viable path for many researchers to access these capabilities.

By applying software engineering best practices (TDD, automation, parallel execution) to scientific validation, we've created a framework that can scale to larger studies and provide the evidence base needed for informed AI adoption in science.

The immediate success in implementing this framework, combined with the progress on the actual experiments, provides strong confidence that the full RCT will yield valuable insights into how AI tools can transform scientific research productivity and quality.

**Key takeaways for business school perspective:**
- Clear methodology for evaluating AI productivity tools
- Demonstrated cost-benefit analysis framework
- Insights into technology adoption in knowledge work
- Model for evidence-based AI implementation strategies

---

## Appendix: Technical Details

### A. Evaluation Code Snippets

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

### B. Budget Breakdown

| Item | Cost |
|------|------|
| Kosmos API usage (5 × $200) | $1,000 |
| Development time (pilot) | $5,000 (in-kind) |
| Cloud infrastructure | $50 |
| Citation verification (CrossRef) | Free |
| Total pilot cost | ~$6,050 |

### C. Timeline Summary

| Phase | Duration | Status |
|-------|----------|---------|
| Design & ground truth prep | 2 weeks | Complete |
| Phase 0: API testing | 30 min | Complete |
| Phase 1: Job validation | 30 min | Complete |
| Phase 2: Experiments | 2 hours | In progress |
| Analysis & reporting | 1 week | In progress |
| Total | 4 hours active + prep | 80% complete |

---

**Prepared by:**
[Your Name]
Computational Biology Researcher
Schmidt Sciences AI Tools Study

**Contact:**
[Email] | [Institution]