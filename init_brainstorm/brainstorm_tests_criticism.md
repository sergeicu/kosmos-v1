# Critical Review: Test Design - Kosmos Pilot Experiments

## Executive Summary
The test design shows good intentions toward TDD but has fundamental flaws in ground truth validity, success criteria justification, and statistical rigor. Several tests can be "gamed" by superficial pattern matching. The 3/5 experiments passing threshold is too lenient and lacks statistical power. Phase 0 doesn't actually test Kosmos capabilities.

## Fatal Flaws (Must Fix Before Execution)

1. **Success Criteria Thresholds Are Arbitrary**
   - **Problem:** 75% recall, 66% trial identification, "at least 3/4 mechanisms" - no justification for these specific numbers
   - **Impact:** Cannot distinguish "good enough" from "barely acceptable". Thresholds may be too easy or impossibly hard.
   - **Evidence:** Document never explains why 75% recall is the target vs. 70% or 80%. Why is 3/4 mechanisms acceptable but 2/4 not?
   - **Fix:** For each threshold, provide justification: baseline performance (random would get X%), competitor tools get Y%, or expert judgment says Z% is minimum useful. If no justification exists, run sensitivity analysis: what if threshold were 60%? 90%?

2. **Ground Truth Validity Not Established**
   - **Problem:** All ground truth datasets are assertions without verification source or date
   - **Impact:** May test Kosmos against outdated or incorrect "known" answers, invalidating entire pilot
   - **Evidence:** Task 1: "Known KRAS targets: SHP2, SOS1, MRTX1133" - according to whom? As of what date? Are there more recent findings post-2023 data cutoff? Task 3: "canonical heat shock genes" - canonical according to which review article?
   - **Fix:** **BLOCKER**: For each ground truth item, cite source (PubMed ID, review article, database). Include date. Have domain expert review and sign off. Check for retractions or updates since ground truth established.

3. **"Simulated Data Option" Undermines Test Validity**
   - **Problem:** Task 3 allows simulated data "if GEO unavailable" - but simulated data with known answers defeats the purpose
   - **Impact:** Kosmos could pattern-match simulated data artifacts instead of demonstrating real analysis capability
   - **Evidence:** Simulation code literally puts heat shock genes at high expression - trivially easy to detect
   - **Fix:** Remove simulation option. Make GEO data access a **prerequisite** for pilot. If GEO truly unavailable, skip Task 3 entirely rather than use fake data.

4. **Spot-Check Sample Size (n=5) Has No Statistical Power**
   - **Problem:** Task 1 validates citations by checking 5 random samples from potentially 20+ citations
   - **Impact:** Could miss 25% fabrication rate with high probability. E.g., if 5/20 citations are fake, probability of drawing all real ones in sample of 5 is ~25%
   - **Evidence:** Basic binomial statistics: cannot detect 20% fabrication rate reliably with n=5 sample
   - **Fix:** Calculate required sample size for detecting 10% fabrication with 90% confidence (likely n=25+). Increase spot-check to 10 citations minimum, or check ALL citations if <15 total.

## Serious Issues (High Risk)

1. **Phase 0 Doesn't Test Kosmos**
   - **Problem:** Phase 0 tests (import SDK, authenticate, basic query) only test API connectivity, not Kosmos capabilities
   - **Likelihood:** High - will give false confidence
   - **Impact:** Could pass Phase 0 with flying colors but discover in Phase 2 that job types don't work as expected
   - **Mitigation:** Rename to "Phase 0: API Connectivity" and add "Phase 0.5: Capability Smoke Tests" that runs minimal version of each job type with trivial query and verifies non-error response.

2. **"Fuzzy Matching" for Mechanisms is Poorly Defined**
   - **Problem:** Task 5 uses fuzzy matching for mechanism identification but algorithm undefined
   - **Likelihood:** Very high - implementation details will matter
   - **Impact:** Could match "synuclein" to "alpha-synuclein propagation via vagus nerve" (correct) or to unrelated "beta-synuclein" paper (false positive). Results not reproducible.
   - **Mitigation:** Define exact matching algorithm: keyword list per mechanism, minimum keywords required, stemming/lemmatization rules. Pre-test algorithm on known positives/negatives.

3. **Notebook Execution ≠ Correct Analysis**
   - **Problem:** Task 3 counts "notebook executed without errors" as success, but code could run and produce garbage
   - **Likelihood:** Medium - depends on Kosmos code quality
   - **Impact:** False positive: declares success when analysis is wrong but code doesn't crash
   - **Mitigation:** Add semantic correctness checks: Does volcano plot have correct axes? Does heatmap cluster heat shock genes together? Are p-values calculated?

4. **Chemical Validity Via SMILES Alone is Insufficient**
   - **Problem:** Task 4 validates molecules solely by "valid SMILES" (RDKit parses it), not chemical plausibility
   - **Likelihood:** High - many invalid molecules have valid SMILES syntax
   - **Impact:** Could pass test with chemically nonsensical but syntactically correct structures
   - **Mitigation:** Add chemical sanity checks: molecular weight in drug-like range (150-800)? Contains unusual elements (radioactive, exotic)? 3D structure can be generated? Passes basic PAINS filters?

5. **Minimum Viable is Only 3/5 Experiments Passing**
   - **Problem:** Success defined as "3/5 benchmark experiments pass ≥75% of assertions" - 60% success rate is "viable"?
   - **Likelihood:** Will definitely be scrutinized
   - **Impact:** Pilot could "pass" with Task 2 and Task 4 completely failing. Not enough evidence for full RCT.
   - **Mitigation:** Require 4/5 experiments pass (80%) for "Minimum Viable". If only 3/5 pass, classify as "Marginal - requires investigation" not "viable".

## Moderate Concerns (Should Address)

1. **Kendall's Tau with Small n Questionable**
   - **Problem:** Task 5 uses Kendall's tau to correlate intervention rankings, but with n=4 interventions, statistical significance is weak
   - **Impact:** Correlation could be 0.5 (target) by chance. Not enough power to distinguish good from random ranking.
   - **Recommendation:** Either increase number of interventions to rank (n=8-10) or acknowledge ranking correlation is exploratory, not definitive metric.

2. **"At Least 1/3 Molecules Shows Improvement" is Very Low Bar**
   - **Problem:** Task 4 passes if even ONE of three molecules is better than baseline
   - **Impact:** 33% success rate for molecule design seems too forgiving
   - **Recommendation:** Require 2/3 molecules show improvement (66% success) for practical utility.

3. **Success Criteria Lack Confidence Intervals**
   - **Problem:** All metrics are point estimates with no uncertainty quantification
   - **Impact:** Cannot assess reliability of measurements
   - **Recommendation:** For each metric, calculate 95% CI. E.g., "75% recall (95% CI: 60-87%)" gives much better picture than "75%".

4. **Expert Review Protocol Undefined**
   - **Problem:** "Expert reviewers rate outputs ≥4/5 for proposal relevance" but no rubric, training, or inter-rater reliability plan
   - **Impact:** Subjective ratings could be inconsistent or biased
   - **Recommendation:** Create detailed rubric for 1-5 scale with examples. Have 2 experts rate same output independently. Calculate Cohen's kappa for agreement.

5. **No Negative Controls**
   - **Problem:** All tests assume Kosmos will produce some output. No tests for how it handles bad inputs (malformed data, impossible queries)
   - **Impact:** May not discover failure modes
   - **Recommendation:** Add 1-2 negative control queries per task: "Analyze this empty CSV", "What papers discuss time-traveling quarks?". Expect graceful failure or "insufficient data" response.

## Minor Issues (Nice to Have)

1. **Time Estimates Don't Include Human Review**
   - **Problem:** Task estimates (15 min, 30 min, 45 min) appear to be Kosmos runtime only, excluding human evaluation time
   - **Recommendation:** Add "+ 15 min evaluation" to each estimate for realism.

2. **No Plan for Dealing with Ties in Metrics**
   - **Problem:** What if recall is exactly 74.5% (rounds to 75%)? Pass or fail?
   - **Recommendation:** Define rounding rules or use strict inequality (>75% not ≥75%).

3. **Citation Verification Assumes DOI Availability**
   - **Problem:** CrossRef API works for DOIs, but what if Kosmos cites papers without DOIs (older papers, books)?
   - **Recommendation:** Have fallback verification (PubMed lookup, manual search) for non-DOI citations.

## Strengths (What's Good)

1. **TDD Philosophy Stated** - "Write tests first, watch fail" is correct approach
2. **Mix of Quantitative and Qualitative** - Automated metrics + expert review is appropriate
3. **Specific Ground Truth Examples** - Concrete targets/trials/genes make tests reproducible
4. **Diverse Metrics Per Task** - Not just accuracy; also completeness, validity, execution success
5. **Spot-Check Strategy** - Citation verification via sampling is pragmatic given constraints
6. **Failure Mode Documentation** - "If Job Fails" sections show planning for negative outcomes

## Unanswered Questions

1. **What is the statistical power to detect true effect size?** With n=5 experiments, can we reliably distinguish 70% vs 80% Kosmos performance?
2. **How were ground truth datasets curated?** Who selected these specific targets/trials/genes and when?
3. **What if Kosmos output format changes between tasks?** Parsing code may break.
4. **Are ground truths comprehensive or exemplar?** E.g., are SHP2, SOS1, MRTX1133 the ONLY valid targets or just examples?
5. **What constitutes "execution success" for notebook?** Exit code 0? All cells run? No exceptions?
6. **How to handle Kosmos output that is correct but not in ground truth?** E.g., identifies real KRAS target not in our list.
7. **What if expert reviewers disagree (one rates 3/5, another rates 5/5)?** Averaging? Consensus discussion?

## Recommended Changes

### Critical (Blockers)
- [ ] **Justify all success thresholds** (75%, 66%, 3/4, etc.) with baseline/competitor data or expert judgment
- [ ] **Cite sources for all ground truth items** with PubMed IDs and dates
- [ ] **Remove simulated data option** - make real GEO data mandatory or skip Task 3
- [ ] **Increase citation spot-check to n=10 minimum** or calculate proper sample size
- [ ] **Have domain expert review and sign off on ground truth** for each task

### High Priority
- [ ] Define exact "fuzzy matching" algorithm for mechanisms/gene names with test cases
- [ ] Add semantic correctness checks for notebook execution (not just "runs without error")
- [ ] Add chemical sanity checks for molecules beyond SMILES validity
- [ ] Increase minimum viable to 4/5 experiments passing (not 3/5)
- [ ] Create expert review rubric with inter-rater reliability plan

### Medium Priority
- [ ] Add Phase 0.5: Capability smoke tests (not just API connectivity)
- [ ] Define what counts as ground truth "match" - exact string match? Synonym list? Ontology?
- [ ] Add 1-2 negative control tests per task for failure mode testing
- [ ] Calculate required sample sizes for statistical power
- [ ] Specify how to handle edge cases (ties, novel findings, format changes)

## Overall Risk Assessment

**Execution Risk:** Medium - Tests can run but may produce misleading results
**Scientific Validity Risk:** **High** - Ground truth validity and statistical power are questionable
**Timeline Risk:** Low - Test design doesn't affect timeline directly
**Budget Risk:** Low - No budget implications from test design

## Verdict

**GO WITH CONDITIONS**

**Justification:** The overall test structure is sound (phased approach, multiple metrics, diverse tasks), but implementation details have serious flaws that could invalidate results. The pilot can proceed if conditions are met, but findings must be interpreted cautiously.

**Mandatory conditions before execution:**
1. All ground truth items must have cited sources and expert sign-off
2. Success criteria thresholds must have written justification (even if "expert judgment")
3. Remove simulated data option for Task 3 - real data only
4. Increase citation spot-check sample size to n=10 minimum
5. Define fuzzy matching algorithm explicitly

**Recommended conditions (strongly advised):**
6. Increase minimum viable to 4/5 experiments (not 3/5)
7. Add capability smoke tests to Phase 0
8. Create expert review rubric before recruiting reviewers
9. Add chemical sanity checks beyond SMILES validity
10. Add semantic checks for notebook execution

**If conditions not met:** Results will be exploratory only, not definitive. Cannot use pilot to justify full RCT deployment without additional validation.

**Key insight:** Current design optimizes for "pilot can complete" over "pilot produces valid evidence". Rebalance toward validity even if it means some tasks might fail.
