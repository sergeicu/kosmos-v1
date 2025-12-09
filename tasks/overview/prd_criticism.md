# Critical Review: PRD - Kosmos RCT Pilot Testing System

## Executive Summary
The PRD attempts to be comprehensive but has critical gaps in metrics definition, budget justification, and risk assessment. The $1000 budget appears arbitrary with no breakdown. Success metrics mix quantitative targets with undefined qualitative criteria. The 4-hour timeline conflicts with detailed technical requirements.

## Fatal Flaws (Must Fix Before Execution)

1. **Budget Has No Detailed Breakdown**
   - **Problem:** States "$1000 (5 experiments × $200/run)" but provides no evidence that each run costs exactly $200
   - **Impact:** Budget could be wildly off. What if MOLECULES costs $400 and LITERATURE costs $50? What about retries? Dataset acquisition? Expert reviewer compensation?
   - **Evidence:** Risk table mentions "Hard stop at $1000 budget" but no itemized costs. "$200/run" appears to be assumption, not verified quote.
   - **Fix:** **BLOCKER**: Get actual pricing from Edison/FutureHouse for each job type. Add line items: 5 Kosmos runs ($X), dataset acquisition ($Y), expert reviewer fees ($Z), contingency for failures (20% = $W). Total must have justification.

2. **"≥75% Ground Truth Recall" Has No Baseline Context**
   - **Problem:** Target of 75% recall appears arbitrary without comparison to random baseline, human performance, or competitor tools
   - **Impact:** Cannot interpret if 75% is good, mediocre, or excellent. Could pass tests with mediocre performance.
   - **Evidence:** Table states "≥75% known items found" but never explains why 75% not 60% or 90%
   - **Fix:** For each quantitative metric, document: (1) Random baseline (X%), (2) Human expert performance (Y%), (3) Why target Z% is meaningful threshold. If no data available, mark as "exploratory threshold - will revise based on Phase 1 results".

3. **Expert Review Process Completely Undefined**
   - **Problem:** Qualitative metrics depend on "Manual Expert Review" with Likert 1-5 scale, but no details on: Who? How many? What domains? How recruited? Compensation? Blind review? Timeline?
   - **Impact:** Cannot execute qualitative evaluation. Entire qualitative success criteria unverifiable.
   - **Evidence:** Table lists "Proposal relevance ≥4/5" and "Actionability ≥4/5" but no expert review protocol anywhere in document
   - **Fix:** **BLOCKER**: Create expert review protocol section: (1) Recruit 2-3 experts (name domains), (2) Define compensation ($X/hour), (3) Create review rubric with examples for each score 1-5, (4) Plan for inter-rater reliability, (5) Timeline - when do reviews happen?

4. **Open Questions Are Actually Blockers**
   - **Problem:** Section "Open Questions" lists critical unknowns but treats them as curiosities not blockers
   - **Impact:** Plan proceeds with unresolved dependencies that could halt execution
   - **Evidence:** "Where is Python client documented?" - if no docs exist, Phase 0 cannot start. "Which public datasets best match?" - if unknown, cannot prepare Phase 2 inputs. "Who can provide qualitative evaluation?" - if unknown, cannot measure success.
   - **Fix:** Reclassify "Open Questions" into "Blockers" (must resolve before start) vs. "To Be Determined" (can resolve during execution). Make blocker resolution a prerequisite in timeline.

## Serious Issues (High Risk)

1. **Timeline Discrepancy: 4 Hours Total vs. 2 Hours Per Experiment**
   - **Problem:** Table shows "Phase 2: 2 hours" for 5 experiments, but earlier states each experiment takes 15-45 min. Math doesn't work if done sequentially.
   - **Likelihood:** Very high - will discover during execution
   - **Impact:** Either timeline is wrong (actually 4+ hours for Phase 2) or parallel execution is required (not validated)
   - **Mitigation:** Clarify: Is 2 hours assuming parallel execution? If so, mark parallel execution as prerequisite (to be validated in Phase 0). If sequential, update timeline to 2-4 hours for Phase 2 alone.

2. **"3/5 Experiments Pass" Minimum Is Too Lenient**
   - **Problem:** Success defined as "≥80% experiments complete (4/5)" AND "3/5 experiments pass ≥75% assertions"
   - **Likelihood:** Will be questioned in any presentation/publication
   - **Impact:** Could declare success with 40% failure rate (2/5 experiments failing)
   - **Mitigation:** Require 4/5 experiments pass for "Minimum Viable". If only 3/5 pass, classify as "Marginal - needs investigation".

3. **Cost/Time Section Conflicts with Risk Table**
   - **Problem:** Cost section says "≤2 hours total execution" but risk table mentions "Execution timeout: 2-hour hard deadline, skip low-priority tests"
   - **Likelihood:** High - suggests timeline is aspirational not realistic
   - **Impact:** Tests get skipped, pilot incomplete
   - **Mitigation:** Be honest: target is 2 hours, realistic is 3-4 hours. Budget 4-hour window. If finishes early, great. If not, don't skip tests.

4. **Folder Structure Shows Dates But No Version Control Strategy**
   - **Problem:** Naming convention uses `s{YYYYMMDD}_task{N}` suggesting manual versioning, but no git branching strategy or tag plan
   - **Likelihood:** Medium - matters for reproducibility
   - **Impact:** Cannot reproduce exact experiment conditions. Hard to track which code version produced which results.
   - **Mitigation:** Add section: "Version Control Strategy" - create git tag for each phase completion, commit all results with timestamped branches.

5. **Risk Mitigation for "Citation Fabrication" is "100% Spot-Check" But Earlier Plan Uses 5 Random**
   - **Problem:** Risk table says "Citation fabrication: Low probability, Critical impact, Mitigation: 100% spot-check validation" but test design uses 5 random citations
   - **Likelihood:** Very high - internal inconsistency
   - **Impact:** Confusion during execution about actual requirements
   - **Mitigation:** Fix inconsistency. Either: (a) Commit to 100% citation validation (check every citation), or (b) Update risk mitigation to match reality (spot-check n=10 per experiment).

## Moderate Concerns (Should Address)

1. **Non-Goals May Exclude Critical Proposal Components**
   - **Problem:** "Full proposal generation" is non-goal but partial proposal sections may still need integration testing
   - **Impact:** May validate individual tasks but miss that outputs don't fit together
   - **Recommendation:** Clarify: Are we testing "task utility" or "integration into proposal workflow"? If latter, need integration test.

2. **Experiment Design Section Duplicates Detailed Task Files**
   - **Problem:** PRD lists experiment details that are more comprehensively covered in task1-5 files
   - **Impact:** Maintenance burden - changes must be synced across multiple files
   - **Recommendation:** PRD should reference task files, not duplicate content. "See tasks/task1_cancer_genomics.md for details."

3. **Implementation Phases Are Overly Detailed for PRD**
   - **Problem:** PRD includes TDD cycle details (RED-GREEN-REFACTOR) that belong in implementation plan
   - **Impact:** PRD becomes implementation guide instead of requirements document
   - **Recommendation:** Move Phase 0/1 test details to plan_phase1.md. PRD should state "what" not "how".

4. **Parallel Execution Model Assumes Tools Available**
   - **Problem:** "5 separate Claude Code instances" assumes: (1) Claude Code can be run 5 times, (2) No license restrictions, (3) No resource contention
   - **Impact:** May discover Claude Code doesn't support parallel execution or hits rate limits
   - **Recommendation:** Add to "Open Questions" → "Blockers": Verify Claude Code licensing allows 5 simultaneous instances. Test resource requirements.

5. **Acceptance Criteria Section Missing**
   - **Problem:** "Approval Checklist" exists but no formal acceptance criteria for PRD itself
   - **Impact:** Unclear when PRD is "done" and approved for implementation
   - **Recommendation:** Add "PRD Acceptance Criteria": All blockers resolved, expert reviewers recruited, budget approved by PI, timeline confirmed feasible.

## Minor Issues (Nice to Have)

1. **No Rollback Plan**
   - **Problem:** Risk table mentions mitigation but no rollback if mitigation fails
   - **Recommendation:** Add "If X happens and mitigation fails, we will: pause/pivot/cancel".

2. **No Data Retention Policy**
   - **Problem:** Will Kosmos outputs be kept? For how long? Privacy concerns?
   - **Recommendation:** Add brief section on data management (where stored, how long, who has access).

3. **No Publication Plan Details**
   - **Problem:** Mentions presentation but not publication strategy
   - **Recommendation:** Will results be published? Conference paper? Internal report? Preprint? Define early.

## Strengths (What's Good)

1. **Clear Goals and Non-Goals** - Scope is well-defined
2. **Quantitative Success Metrics** - Specific numerical targets
3. **Folder Structure Diagram** - Helps implementation
4. **Risk Table** - Shows awareness of failure modes
5. **Deliverables List** - Clear outputs defined
6. **Timeline Breakdown** - Phased approach with time estimates

## Unanswered Questions

1. **What is Schmidt Sciences' actual evaluation criteria for RCT tools?** Does pilot align?
2. **Who approves this PRD?** PI? Grant manager? Schmidt Sciences program officer?
3. **What happens to pilot results?** Feed into full RCT? Published independently?
4. **Are there IRB/ethics considerations** for testing on human participants (RCT users)?
5. **What is definition of "proposal-relevant subtask"?** Background section? Methods? Aims? All of above?
6. **How does 4-hour pilot validate 2-week proposal workflow?** What's the connection?
7. **What if Edison API deprecates features mid-pilot?** Version lock possible?
8. **Are expert reviewers volunteers or paid?** Budget implications.

## Recommended Changes

### Must Fix (Blockers)
- [ ] **Get itemized pricing from Edison** for each job type and create detailed budget
- [ ] **Document baseline/comparison for all quantitative targets** (why 75%? compared to what?)
- [ ] **Create expert review protocol** with recruitment plan, compensation, rubric, timeline
- [ ] **Reclassify "Open Questions"** into Blockers vs. TBD - resolve blockers before start
- [ ] **Fix citation validation inconsistency** (100% vs spot-check n=5)

### High Priority
- [ ] Clarify timeline: parallel vs sequential execution, realistic vs aspirational
- [ ] Increase minimum viable to 4/5 experiments passing (not 3/5)
- [ ] Add version control strategy (git tags, branching, reproducibility)
- [ ] Verify Claude Code supports 5 parallel instances
- [ ] Add PRD acceptance criteria and approval process

### Medium Priority
- [ ] Move TDD implementation details to plan_phase1.md (keep PRD high-level)
- [ ] Add data retention and privacy policy section
- [ ] Define integration testing approach if needed
- [ ] Add rollback plan for each risk if mitigation fails
- [ ] Clarify what "proposal-relevant" means specifically

## Overall Risk Assessment

**Execution Risk:** **High** - Multiple unresolved blockers (budget, expert reviewers, open questions)
**Scientific Validity Risk:** Medium - Metrics defined but baselines missing
**Timeline Risk:** **High** - 4-hour timeline appears unrealistic for 5 experiments + review
**Budget Risk:** **High** - $1000 is assertion not justified estimate

## Verdict

**NO-GO (Until Blockers Resolved)**

**Justification:** The PRD has good structure and clear goals, but critical prerequisites are undefined. Cannot approve implementation when budget is unjustified, expert reviewers unidentified, and success baselines arbitrary. The "Open Questions" section reveals this is a draft, not a ready-for-execution plan.

**Required for GO:**
1. Itemized budget with actual Edison pricing + expert fees + contingency
2. Expert review protocol with identified reviewers and confirmed availability
3. Justification for quantitative thresholds (75%, 80%, etc.) with baselines
4. Resolution of all "blocker" open questions (SDK docs, dataset access)
5. Realistic timeline (acknowledge 4+ hours realistic, not 2 hours)

**After resolving blockers, verdict becomes: GO WITH CONDITIONS**
- Condition: Parallel execution validated in Phase 0 before Phase 2 start
- Condition: Version control strategy implemented for reproducibility
- Condition: Minimum viable increased to 4/5 experiments (not 3/5)
- Condition: Add formal PRD acceptance/approval before implementation begins

**Recommendation:** This PRD should go through approval cycle with PI/grant manager. Current version reads as planning document, not approved requirements. Add signature/approval section: "Approved by: [PI name], Date: [date]".
