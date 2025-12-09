# Task 0: Critical Review - Red Team Analysis

## Objective
Perform adversarial review of the Kosmos testing plan to identify flaws, unrealistic assumptions, missing requirements, and failure modes BEFORE execution.

## Context
You are a critical reviewer with deep expertise in:
- Experimental design and statistics
- API integration and failure modes
- Scientific benchmarking methodology
- Computational biology domain knowledge
- Software testing and TDD practices

Your job is to **find problems**, not validate the plan. Be ruthlessly critical.

---

## Your Task

### 1. Review All Planning Documents

**Read thoroughly:**
- `brainstorm/brainstorm_user_needs.md`
- `brainstorm/brainstorm_tools.md`
- `brainstorm/brainstorm_tests.md`
- `tasks/overview/prd.md`
- `tasks/overview/plan_phase1.md`
- `tasks/task1_cancer_genomics.md`
- `tasks/task2_immunology.md`
- `tasks/task3_systems_bio.md`
- `tasks/task4_structural_bio.md`
- `tasks/task5_neuroscience.md`

### 2. Critical Review Framework

For each document, evaluate:

#### A. **Realism**
- Are timelines achievable? (e.g., 15 min for complex literature synthesis)
- Are success criteria too lenient? (e.g., 75% recall - is that actually good?)
- Are ground truth datasets obtainable?
- Is the budget realistic? ($200/run - what if jobs fail?)

#### B. **Rigor**
- Are metrics well-defined and measurable?
- Are ground truths comprehensive or cherry-picked?
- Can automated evaluation actually work? (e.g., "fuzzy matching" for gene names)
- Are there confounding variables?

#### C. **Failure Modes**
- What happens if API rate limits hit?
- What if Kosmos returns unusable output format?
- What if ground truth data doesn't match Kosmos input requirements?
- What if 3/5 experiments fail - is pilot still valid?

#### D. **Missing Components**
- Are there unstated dependencies? (e.g., expert reviewers, dataset access)
- Are there missing test cases? (e.g., edge cases, malformed inputs)
- Are there missing quality checks? (e.g., statistical significance tests)

#### E. **Domain Expertise**
- Are ground truths actually correct? (e.g., are those the canonical heat shock genes?)
- Are queries well-formulated for the domain?
- Would a computational biologist actually find this useful?

#### F. **TDD Compliance**
- Does the plan actually follow TDD? (tests first, watch fail, minimal code)
- Are there risks of writing code before tests?
- Are test assertions specific enough?

---

### 3. Generate Criticism Files

Create the following files with **specific, actionable critiques**:

#### `brainstorm/brainstorm_user_needs_criticism.md`
- Are user needs actually validated or assumed?
- Is the persona too narrow? (early-career comp bio only)
- Are pain points evidence-based?

#### `brainstorm/brainstorm_tools_criticism.md`
- Are tool capabilities verified or based on marketing materials?
- Are limitations underestimated?
- Is the testing stack appropriate?

#### `brainstorm/brainstorm_tests_criticism.md`
- Is the test design philosophy sound?
- Are success criteria too easy to game?
- Are there statistical power issues?

#### `tasks/overview/prd_criticism.md`
- Is the PRD complete? (missing acceptance criteria, stakeholder sign-off)
- Are metrics SMART (Specific, Measurable, Achievable, Relevant, Time-bound)?
- Are risks adequately addressed?
- Is the budget breakdown detailed?

#### `tasks/overview/plan_phase1_criticism.md`
- Is the TDD cycle realistic for time-constrained pilot?
- Are test implementations actually minimal?
- Are there circular dependencies in the plan?

#### `tasks/task1_cancer_genomics_criticism.md`
Critique:
- Ground truth completeness (are there more recent targets post-2023?)
- Citation validation method (CrossRef API reliable for all journals?)
- Metric targets (is 75% recall good enough? what's the baseline?)
- Query formulation (too broad? too narrow?)
- Spot-check sample size (is 5 citations statistically valid?)

#### `tasks/task2_immunology_criticism.md`
Critique:
- Clinical trial search scope (ClinicalTrials.gov only? what about EudraCT, ICTRP?)
- Precedent definition (what counts as "developed"? preclinical vs. clinical?)
- Binary accuracy metric (yes/no too simplistic?)
- Outcome completeness (how to measure objectively?)

#### `tasks/task3_systems_bio_criticism.md`
Critique:
- Dataset availability (is GEO data actually accessible via API?)
- Simulated data option (defeats purpose of real-world test?)
- Notebook execution assumption (what if code has bugs but runs?)
- Hypothesis evaluation (keyword matching too naive?)
- 45-minute runtime (enough for complex analysis?)

#### `tasks/task4_structural_bio_criticism.md`
Critique:
- Chemical validity (RDKit validation sufficient? what about 3D stereochemistry?)
- ADMET predictions (computational estimates vs. experimental - how reliable?)
- Baseline comparison (nirmatrelvir properties - are these verified?)
- Improvement metric (is 1/3 molecules showing improvement acceptable?)
- Retrosynthesis evaluation (how to validate routes are realistic?)

#### `tasks/task5_neuroscience_criticism.md`
Critique:
- Cross-domain synthesis difficulty (is this too hard for 15 min?)
- Mechanism fuzzy matching (will this work reliably?)
- Ranking correlation (Kendall's tau with small n?)
- Primary research detection (heuristic too simple?)
- Ground truth bias (are these the only established mechanisms?)

#### `tasks/overall_methodology_criticism.md`
Critique:
- Parallel execution assumption (can API handle 5 simultaneous jobs?)
- TDD discipline (will time pressure lead to shortcuts?)
- Expert review availability (who are these experts? how recruited?)
- Publication bias (ground truths based on published literature)
- Generalizability (5 domains enough to represent all comp bio?)

---

### 4. Criticism File Template

Use this structure for each `_criticism.md` file:

```markdown
# Critical Review: {Document Name}

## Executive Summary
{2-3 sentences: biggest problems, overall assessment}

## Fatal Flaws (Must Fix Before Execution)
1. **{Issue}**
   - **Problem:** {What's wrong}
   - **Impact:** {Why it matters}
   - **Evidence:** {How you know}
   - **Fix:** {Specific action to resolve}

## Serious Issues (High Risk)
1. **{Issue}**
   - **Problem:** {What's wrong}
   - **Likelihood:** {Probability of occurring}
   - **Impact:** {Consequence if occurs}
   - **Mitigation:** {How to reduce risk}

## Moderate Concerns (Should Address)
1. **{Issue}**
   - **Problem:** {What's wrong}
   - **Impact:** {Effect on pilot}
   - **Recommendation:** {Suggested improvement}

## Minor Issues (Nice to Have)
1. **{Issue}**
   - **Problem:** {What's wrong}
   - **Recommendation:** {Optional improvement}

## Strengths (What's Good)
1. {Positive aspect}
2. {Positive aspect}

## Unanswered Questions
1. {Question that plan doesn't address}
2. {Question that plan doesn't address}

## Recommended Changes
- [ ] {Specific action item}
- [ ] {Specific action item}

## Overall Risk Assessment
**Execution Risk:** {Low/Medium/High/Critical}
**Scientific Validity Risk:** {Low/Medium/High/Critical}
**Timeline Risk:** {Low/Medium/High/Critical}
**Budget Risk:** {Low/Medium/High/Critical}

## Verdict
{GO / NO-GO / GO WITH CONDITIONS}
{Justification}
```

---

### 5. Specific Review Checklist

**For each task prompt, verify:**

- [ ] Ground truth is independently verifiable (not circular)
- [ ] Metrics have clear pass/fail thresholds
- [ ] Success criteria aren't gamed by Kosmos output format
- [ ] Failure modes have documented recovery paths
- [ ] Time estimates include buffer for debugging
- [ ] Budget includes contingency for retries
- [ ] Dependencies are explicitly stated
- [ ] Evaluation code is testable (TDD for the tests!)
- [ ] Report templates don't assume success
- [ ] Query formulation is domain-appropriate

**For the overall plan:**

- [ ] Phase 0/1 tests are actually sufficient
- [ ] Parallel execution doesn't introduce race conditions
- [ ] Aggregation methodology is defined
- [ ] Expert review process is detailed
- [ ] Statistical power is adequate (n=5?)
- [ ] Publication/presentation plan exists
- [ ] Ethical considerations addressed (if any)
- [ ] Data retention/privacy plan exists

---

### 6. Red Team Scenarios

**Stress-test the plan by simulating:**

1. **API Disaster:** Edison API is down for 4 hours during pilot
   - Does plan have fallback?
   - How to reschedule?

2. **Format Chaos:** Kosmos returns JSON in unexpected schema
   - Will parsing code break?
   - Is error handling robust?

3. **Ground Truth Invalidation:** Paper retracts a key "known" target mid-pilot
   - How to handle?
   - Does this invalidate results?

4. **Time Overrun:** Task 3 takes 90 min instead of 45 min
   - Does this derail entire pilot?
   - Budget for compute time?

5. **Quality Disaster:** All 5 experiments return gibberish
   - Is this a Kosmos failure or query failure?
   - How to diagnose?

6. **Citation Fabrication:** Spot-check finds 2/5 citations are fake
   - Immediate fail, or continue?
   - What's the escalation path?

7. **Expert Unavailability:** Reviewers ghost the qualitative evaluation
   - Pilot still valid?
   - Can quantitative metrics stand alone?

Document responses to each scenario.

---

### 7. Domain Expert Consultation

**Identify questions that require expert input:**

- Computational biology expert: Are these ground truths current and complete?
- Statistics expert: Is n=5 adequate? What's statistical power?
- API/infrastructure expert: Is 2-hour parallel execution realistic?
- Grant reviewer: Would this pilot satisfy Schmidt Sciences requirements?

List these in each criticism file under "Unanswered Questions."

---

## Deliverables

### Primary Outputs (Required)
1. `brainstorm/brainstorm_user_needs_criticism.md`
2. `brainstorm/brainstorm_tools_criticism.md`
3. `brainstorm/brainstorm_tests_criticism.md`
4. `tasks/overview/prd_criticism.md`
5. `tasks/overview/plan_phase1_criticism.md`
6. `tasks/task1_cancer_genomics_criticism.md`
7. `tasks/task2_immunology_criticism.md`
8. `tasks/task3_systems_bio_criticism.md`
9. `tasks/task4_structural_bio_criticism.md`
10. `tasks/task5_neuroscience_criticism.md`
11. `tasks/overall_methodology_criticism.md`

### Summary Output
12. `tasks/CRITICAL_REVIEW_SUMMARY.md`
    - Aggregate all fatal flaws
    - Overall GO/NO-GO recommendation
    - Prioritized fix list
    - Revised timeline/budget estimates

---

## Success Criteria

**This review is successful if:**
- [ ] ≥3 fatal flaws identified per document (if perfect, you're not looking hard enough)
- [ ] All fatal flaws have specific fixes proposed
- [ ] Red team scenarios expose ≥2 undocumented failure modes
- [ ] Unanswered questions list reveals missing stakeholders
- [ ] Overall recommendation is evidence-based and actionable
- [ ] Criticism is **constructive**, not just negative

**This review fails if:**
- Critique is vague ("might not work")
- No specific fixes proposed
- No strengths identified (everything sucks = lazy review)
- No distinction between fatal vs. minor issues
- Criticism is personal rather than technical

---

## Tone and Approach

**Be:**
- **Adversarial but fair:** Find real problems, not nitpicks
- **Specific:** "75% recall is too low because..." not "metrics are bad"
- **Evidence-based:** Cite sources, precedents, or logical reasoning
- **Actionable:** Every critique has a fix or mitigation

**Don't be:**
- Dismissive ("this whole plan is garbage")
- Pedantic (formatting issues, typos)
- Unrealistic (demanding perfection)
- Outside scope (critiquing grant itself, not testing plan)

---

## Red Flags to Look For

### Common Planning Mistakes
- **Optimism bias:** "This will only take 15 minutes" (says who?)
- **Happy path only:** No error handling documented
- **Circular ground truth:** Using Kosmos output to validate Kosmos
- **Undefined "quality":** "High-quality" analysis (measured how?)
- **Magic numbers:** "75%" (why not 70% or 80%?)
- **TDD theater:** Tests written after code, calling it TDD
- **Resume-driven development:** Using tools because they're cool, not appropriate

### Scientific Red Flags
- **Cherry-picked ground truth:** Only easy-to-find examples
- **Outdated baselines:** 2021 papers when it's 2025
- **Domain mismatch:** Neuroscience query evaluated by cancer biologist
- **Publication bias:** Ignoring negative results or failed approaches
- **Statistical naivete:** No power analysis, multiple testing correction

### Engineering Red Flags
- **No error budgets:** Assume 100% uptime
- **Tight coupling:** One failure cascades to all 5 experiments
- **Missing observability:** Can't diagnose why Kosmos failed
- **No rollback plan:** Can't recover from bad state
- **Assumption of competence:** "Just use RDKit" (but no one knows RDKit)

---

## Timeline

**Estimated time:** 2-3 hours for thorough review

**Breakdown:**
- 1 hour: Read all documents (skim first, deep read second)
- 1 hour: Write criticism files (use template, fill in specifics)
- 30 min: Red team scenarios
- 30 min: Summary and overall recommendation

---

## Acceptance Criteria

**Review is complete when:**
- All 12 deliverables exist
- Each has ≥3 fatal/serious issues identified
- Each has ≥2 strengths identified (balance)
- Summary provides clear GO/NO-GO with justification
- Fixes are prioritized (must-fix vs. nice-to-have)
- Timeline/budget revisions proposed if needed

---

## Final Note

**Your goal is to IMPROVE the plan, not kill it.**

A good critical review finds fixable problems BEFORE they become unfixable disasters during execution. Be tough, but be fair. The team wants this to succeed - help them succeed by finding the landmines now.

**Red team motto:** "I'm not your enemy, I'm your parachute."
