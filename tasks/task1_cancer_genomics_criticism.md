# Critical Review: Task 1 - Cancer Genomics (LITERATURE Job)

## Executive Summary
The task has well-defined structure but critical flaws in ground truth validity and evaluation metrics. The "known targets" from 2024 may already be outdated by execution date. Citation spot-check (n=5) has insufficient statistical power. Query asks for "last 3 years" but Kosmos corpus date is unknown. Success depends on 3/4 metrics but thresholds are arbitrary.

## Fatal Flaws (Must Fix Before Execution)

1. **Ground Truth Will Be Outdated by Execution**
   - **Problem:** Ground truth lists "Known KRAS-mutant PDAC targets (as of 2024)" but provides no source citation or date-of-publication for these assertions
   - **Impact:** Cannot verify if SHP2, SOS1, MRTX1133, MRTX849, RM-018 are actually the most promising targets as of Dec 2024, or if this list is from early 2024, mid-2024, etc. Could test Kosmos against incorrect ground truth.
   - **Evidence:** No PubMed IDs, no review article citation. Comment "// MRTX1133 Nature 2023" provides DOI but doesn't confirm this is still state-of-art in 2024/2025
   - **Fix:** **BLOCKER**: Cite source for ground truth list. Consult pancreatic cancer expert to validate list is current as of pilot execution date. If no expert available, cite recent review article (2024) and state "targets per [Author] et al 2024".

2. **Query Asks for "Last 3 Years" But Kosmos Corpus Date Unknown**
   - **Problem:** Query requests targets "identified in the last 3 years" but if Kosmos literature corpus ends in 2023, it cannot accurately answer a query run in late 2024
   - **Impact:** Will unfairly penalize Kosmos for missing 2024 publications. Or Kosmos may hallucinate 2024 findings.
   - **Evidence:** Tools assessment states "Time window unknown (last update?)" - this is unresolved blocker
   - **Fix:** **BLOCKER**: Verify Kosmos/PaperQA3 corpus cutoff date. If pre-2024, adjust query to "identified between 2021-2023" to match corpus coverage. Update ground truth accordingly.

3. **Spot-Check n=5 Cannot Detect Meaningful Fabrication Rates**
   - **Problem:** Statistical power analysis: with n=5 sample from 20 citations, 95% confidence interval for 0/5 fabrications is 0-43% fabrication rate
   - **Impact:** Could have 20-30% citation fabrication and still pass spot-check with reasonable probability
   - **Evidence:** Basic binomial stats: if true fabrication rate is 20%, probability of drawing 5 all-real citations is (0.8)^5 = 33%
   - **Fix:** Increase spot-check to minimum n=10 (if 20 total citations). Better: check ALL citations if <15 total. Document confidence interval for fabrication rate estimate.

4. **"Key Paper Coverage ≥66%" Threshold Has No Justification**
   - **Problem:** Why is citing 2/3 key papers acceptable? What if the missing paper contains critical recent findings?
   - **Impact:** Could pass metric while missing most important recent publication (e.g., 2024 breakthrough)
   - **Evidence:** No rationale for 66% vs 75% or 100%
   - **Fix:** Either require 100% key paper coverage (only 3 papers - should be findable), or justify why 66% is acceptable threshold (e.g., "one paper may be behind paywall Kosmos can't access").

## Serious Issues (High Risk)

1. **Target Recall 75% Based on Possibly Incomplete Ground Truth**
   - **Problem:** "Known targets" list may not be exhaustive - could be exemplar targets not comprehensive list
   - **Likelihood:** High - cancer research moves fast, new targets published frequently
   - **Impact:** Kosmos could identify valid new target not in ground truth and get marked wrong (false negative)
   - **Mitigation:** Clarify: is ground truth "minimum required" or "comprehensive"? Add evaluation for novel targets found: "Flag for expert review: are these plausible new targets?"

2. **Citation Validation via CrossRef May Miss Fabricated Papers**
   - **Problem:** CrossRef API confirms DOI exists, but doesn't verify paper actually discusses KRAS/PDAC
   - **Likelihood:** Medium - if Kosmos fabricates, likely uses real DOI for irrelevant paper
   - **Impact:** False negative on fabrication detection
   - **Mitigation:** Add semantic check: for each sampled citation, verify title contains "KRAS" OR "pancreatic cancer" OR related terms. DOI existence alone insufficient.

3. **15-Minute Runtime May Be Too Short for Quality Synthesis**
   - **Problem:** Query asks for "mechanisms underlie resistance to current targeted therapies" which is complex, multi-part question
   - **Likelihood:** High - complex queries take longer
   - **Impact:** Kosmos may timeout or provide superficial answer to meet deadline
   - **Mitigation:** Allow 20-25 minutes runtime. If Kosmos consistently finishes in 15 min, great. If not, don't penalize for taking appropriate time.

4. **"Resistance Mechanisms" Ground Truth Lacks Specificity**
   - **Problem:** Ground truth lists 4 broad mechanism categories but query asks for specific mechanisms underlying resistance
   - **Likelihood:** High - matching will be subjective
   - **Impact:** Unclear if "KRAS G12D/V bypass signaling" should match to specific proteins or pathways
   - **Mitigation:** Expand ground truth resistance mechanisms to protein/gene level (e.g., "MEK reactivation via [specific MEK isoforms]"). Or acknowledge this metric is qualitative only.

## Moderate Concerns (Should Address)

1. **Success Criteria "≥3/4 Metrics Pass" Could Mean Missing Critical Ones**
   - **Problem:** Could pass with citation count=25, recall=80%, key papers=100% but citation validity=60% (fabrications)
   - **Impact:** Major failure mode (fabricated citations) could be masked by passing other metrics
   - **Recommendation:** Tier metrics: "Citation validity=100%" is mandatory (cannot fail). Other 3 metrics are "≥2/3 must pass".

2. **"Parse Results" Step Assumes Kosmos Output is Structured**
   - **Problem:** Task says "Extract: Identified targets (List of protein/pathway names)" but format unclear
   - **Impact:** If Kosmos returns prose, not structured list, parsing may fail
   - **Recommendation:** Document expected output schema. If Kosmos doesn't provide structured output, add manual extraction step (timed).

3. **No Baseline Comparison**
   - **Problem:** How does Kosmos performance compare to PubMed search + manual reading?
   - **Impact:** Cannot interpret if 75% recall is good or mediocre
   - **Recommendation:** Add baseline comparison: "Research assistant given 30 min to search PubMed for same query. Compare recall." Or cite competitor tool benchmarks.

4. **Report Template Assumes Success**
   - **Problem:** Template has "✓/✗" fields but heavy emphasis on successful metrics
   - **Impact:** May bias toward positive interpretation
   - **Recommendation:** Add "Critical Failures" section to report: fabricated citations, missing recent targets, factual errors.

## Minor Issues (Nice to Have)

1. **$200 Cost Not Verified**
   - **Problem:** States "Cost: ~$200/run" without source
   - **Recommendation:** Confirm actual LITERATURE job cost with Edison.

2. **30-Minute Timeline Includes Evaluation**
   - **Problem:** "15 min Kosmos + 15 min evaluation" may be tight for thorough analysis
   - **Recommendation:** Budget 45 min total to avoid rushing.

3. **RM-018 in Ground Truth Lacks Context**
   - **Problem:** Other targets have clear status (MRTX1133 = inhibitor), RM-018 not explained
   - **Recommendation:** Add brief description for each ground truth target.

## Strengths (What's Good)

1. **Clear Query Formulation** - Specific disease, timeframe, and two-part question (targets + resistance)
2. **Concrete Ground Truth** - Actual protein names and DOIs
3. **Multiple Evaluation Dimensions** - Not just accuracy; also completeness and citation validity
4. **Failure Handling Specified** - "If Job Fails" section shows planning
5. **Detailed Report Template** - Clear structure for results documentation

## Unanswered Questions

1. **What if Kosmos identifies targets from 2024 papers not in ground truth?** False negative or true positive?
2. **How to handle targets under different names?** (e.g., "SHP2" vs "PTPN11" vs "protein tyrosine phosphatase non-receptor type 11")
3. **What if Kosmos provides targets for KRAS-mutant cancer generally, not PDAC specifically?** Related but not exact match.
4. **Are resistance mechanisms limited to acquired resistance or include intrinsic?** Ground truth doesn't specify.
5. **What happens if Kosmos cites retracted paper?** Counts as fabrication? Valid but problematic?
6. **How current must citations be?** If Kosmos cites 2019 paper on SHP2, is that acceptable or outdated?

## Recommended Changes

### Critical (Blockers)
- [ ] **Verify Kosmos corpus cutoff date** - adjust query if needed ("2021-2023" not "last 3 years")
- [ ] **Cite source for ground truth targets** - expert review or 2024 review article
- [ ] **Validate ground truth is current** as of pilot execution date (not stale 2024-early data)
- [ ] **Increase citation spot-check to n=10** or calculate proper sample size for 95% CI
- [ ] **Justify or remove 66% key paper threshold** (prefer 100% for only 3 papers)

### High Priority
- [ ] Add semantic check to citation validation (title must mention KRAS/pancreatic cancer)
- [ ] Clarify if ground truth is "minimum required" or "comprehensive" target list
- [ ] Tier success criteria: citation validity=100% mandatory, 2/3 other metrics pass
- [ ] Expand resistance mechanisms to protein-level specificity or mark as qualitative
- [ ] Allow 20-25 min runtime buffer (not hard 15 min cutoff)

### Medium Priority
- [ ] Add handling for novel targets not in ground truth (expert review flag)
- [ ] Document expected Kosmos output schema for parsing
- [ ] Add baseline comparison (human performance or competitor tool)
- [ ] Create synonym list for target names (SHP2=PTPN11, etc.)
- [ ] Clarify acquired vs intrinsic resistance scope

## Overall Risk Assessment

**Execution Risk:** Medium - Task can run but metrics may not measure what we think
**Scientific Validity Risk:** **High** - Ground truth validity unverified, could be outdated
**Timeline Risk:** Low - 30 min is reasonable for this task
**Budget Risk:** Low - Single $200 run (if price verified)

## Verdict

**GO WITH CONDITIONS**

**Justification:** The task structure is solid, but ground truth quality is questionable and statistical rigor is lacking. Can proceed if conditions are met, but results must be interpreted carefully. The biggest risk is testing Kosmos against incorrect or outdated "known" answers.

**Mandatory conditions:**
1. Verify and cite source for ground truth targets (expert sign-off or review article)
2. Confirm Kosmos corpus date matches query timeframe ("last 3 years")
3. Increase citation spot-check to n=10 minimum
4. Make citation validity 100% a mandatory metric (cannot pass task with any fabrications in sample)

**Recommended conditions:**
5. Add synonym handling for target names
6. Flag novel targets for expert review (don't automatically mark wrong)
7. Add semantic validation to citation checks
8. Document expected output format before execution
9. Allow 25 min runtime buffer

**If conditions not met:** Results are exploratory only. Cannot claim "Task 1 validates Kosmos for cancer genomics literature synthesis" without addressing ground truth validity and statistical power issues.

**Key insight:** This task conflates two different validations: (1) Can Kosmos find known information (recall test)?, and (2) Can Kosmos synthesize novel insights (discovery test)? Current design only tests #1, but query phrasing suggests #2 is also desired. Clarify which is primary goal.
