# Critical Review: Tools Assessment - Edison Scientific Platform

## Executive Summary
This document reads like marketing material rather than a critical technical assessment. Tool capabilities are listed without verification, limitations are understated, and critical implementation details (versioning, API stability, rate limits) are missing. The testing stack is reasonable but assumes components work without validation plans.

## Fatal Flaws (Must Fix Before Execution)

1. **Tool Capabilities Not Verified**
   - **Problem:** All "Strengths" appear sourced from documentation/marketing without independent verification
   - **Impact:** May discover mid-pilot that advertised capabilities don't work or have undisclosed limitations
   - **Evidence:** "~1500 papers analyzed per run" - no source cited. "79.4% accuracy" - documented where? On what benchmark? "External tool integration" - which tools specifically?
   - **Fix:** **BEFORE Phase 2 execution**: Run smoke tests on each job type to verify advertised capabilities. Document actual behavior vs. claimed behavior. Cite specific source documents for each claim.

2. **No Version/API Stability Information**
   - **Problem:** No mention of which versions of PaperQA3, Phoenix, ChemCrow being used. No API stability guarantees.
   - **Impact:** API changes mid-pilot could break all tests. Results not reproducible.
   - **Evidence:** Document never mentions versioning or changelog access
   - **Fix:** Document exact versions: Edison SDK version, Kosmos model version, underlying tool versions. Check for API versioning policy. Subscribe to breaking changes notifications if available.

3. **Parallel Execution Not Validated**
   - **Problem:** Plan assumes "5 separate Claude Code instances" can run simultaneously without interference, but no verification
   - **Impact:** Could hit rate limits, API throttling, resource contention, or discover parallel execution is blocked by Edison
   - **Evidence:** States "5 separate Claude Code instances" and "Parallel Execution" but no validation plan
   - **Fix:** **Phase 0 requirement**: Test parallel API calls (2-3 simultaneous requests minimum) to verify no rate limiting. Document actual throughput limits. Have sequential fallback plan.

4. **Expert Reviewers Not Identified**
   - **Problem:** Quality metrics depend on "Expert review of scientific quality (1-5 Likert scale)" but no experts recruited
   - **Impact:** Cannot complete qualitative evaluation. Pilot incomplete without this component.
   - **Evidence:** No names, affiliations, expertise areas, or recruitment plan mentioned
   - **Fix:** **Before pilot start**: Recruit and confirm availability of 2-3 domain experts (one per 2 domains minimum). Define compensation/incentives. Create review protocol and timeline.

## Serious Issues (High Risk)

1. **"79.4% Accuracy" is Meaningless Without Context**
   - **Problem:** PaperQA3 accuracy cited as 79.4% but benchmark, metrics, and test set undefined
   - **Likelihood:** High - this will be questioned in any publication/report
   - **Impact:** Cannot interpret if Kosmos results are good/bad relative to documented performance
   - **Mitigation:** Find source of 79.4% figure. Document benchmark name, evaluation metric (precision? recall? F1?), test set composition, date published.

2. **Limitations Severely Understated**
   - **Problem:** LITERATURE "Limited to published literature (no preprints confirmed?)" should be a major limitation, not a question mark
   - **Likelihood:** Very high - preprints are critical for "last 3 years" queries in cancer/COVID research
   - **Impact:** Ground truth may include findings only in preprints, causing false negatives
   - **Mitigation:** Verify preprint coverage ASAP. If no arXiv/bioRxiv coverage, adjust ground truth to exclude preprint-only findings or note as test limitation.

3. **5GB Data Limit for ANALYSIS Could Be Blocking**
   - **Problem:** "5GB uncompressed limit" may be smaller than typical RNA-seq datasets
   - **Likelihood:** Medium - modern RNA-seq can exceed 5GB easily
   - **Impact:** Task 3 may fail due to data size before testing Kosmos capabilities
   - **Mitigation:** Check actual size of E. coli dataset. If >5GB, subsample or use different dataset. Document size limits clearly in task3 prompt.

4. **"No raw sequencing/imaging support" Excludes Common Data Types**
   - **Problem:** Many computational biology workflows start with raw FASTQ or image files
   - **Likelihood:** Medium - depends on whether test datasets are pre-processed
   - **Impact:** Limits applicability to real proposal workflows where researchers have raw data
   - **Mitigation:** Explicitly document that pilot only tests analysis of pre-processed data. Note as limitation in final report.

## Moderate Concerns (Should Address)

1. **Undefined "Typical" Execution Time**
   - **Problem:** ANALYSIS states "3-10 min execution typical" - wide range, no source, unclear if includes Kosmos overhead
   - **Impact:** Timeline assumptions may be off by 3x
   - **Recommendation:** Add buffer: assume 15 min for 10 min "typical" case. Monitor actual times in Phase 1.

2. **Ground Truth Source Quality Unverified**
   - **Problem:** "Manual curation" of ground truth - who curates? What expertise required?
   - **Impact:** Poor ground truth = invalid benchmarks
   - **Recommendation:** Each ground truth dataset should have expert reviewer sign-off with credentials documented.

3. **PRECEDENT Search Scope Undefined**
   - **Problem:** "Search scope unclear (PubMed? bioRxiv?)" is acknowledged but not resolved
   - **Impact:** Cannot interpret recall metrics if don't know search space
   - **Recommendation:** **Phase 0 test**: Run precedent query with known answer and inspect sources cited. Document actual databases searched.

4. **Infrastructure Requirements Too Vague**
   - **Problem:** "Shared task definition format (Markdown)" and "Isolated output directories" - no specs provided
   - **Impact:** Implementation delays when trying to set up parallel execution
   - **Recommendation:** Create detailed folder structure diagram with file naming conventions before Phase 1.

## Minor Issues (Nice to Have)

1. **No Mention of Cost Per Job Type**
   - **Problem:** States "$200/run" overall but doesn't break down by job type (LITERATURE vs MOLECULES may differ)
   - **Recommendation:** Get cost breakdown from Edison. Budget may need adjustment.

2. **"Public datasets (GEO, ArrayExpress)" - Access Method Undefined**
   - **Problem:** How will datasets be downloaded? GEO API? Manual? What if access fails?
   - **Recommendation:** Document GEO accession numbers and test download before pilot.

3. **Citation Validation Method Assumed**
   - **Problem:** "Citation validation" listed under automated metrics but no tool/API specified
   - **Recommendation:** Specify CrossRef API (as used in task prompts). Test rate limits.

## Strengths (What's Good)

1. **Clear Job Type Taxonomy** - 4 distinct job types (LITERATURE, ANALYSIS, PRECEDENT, MOLECULES) well-defined
2. **Phased Testing Approach** - Phase 0 → 1 → 2 progression is sound
3. **Mix of Automated and Manual Metrics** - Recognizes both quantitative and qualitative evaluation needed
4. **TDD Commitment** - Explicit "Write failing tests first" in testing stack
5. **Explicit Limitations Section** - Shows some critical thinking, even if incomplete

## Unanswered Questions

1. **What is the Edison Python SDK installation process?** PyPI package? Private repo? Version constraints?
2. **Are there API rate limits per user/key?** What are they? How to monitor?
3. **What happens if a job times out mid-execution?** Can it be resumed? Restarted? Refund?
4. **Is there a job queue system?** Do jobs run immediately or queue with unknown wait time?
5. **Can we monitor job progress in real-time?** Or only see results after completion?
6. **What is the actual literature corpus date range?** "Last update unknown" could mean 2021 or 2024 data.
7. **Do MOLECULES predictions include experimental uncertainty?** Or just point estimates?
8. **What is the retry policy for failed API calls?** Auto-retry? Manual only?

## Recommended Changes

- [ ] **PHASE 0 BLOCKER**: Verify parallel API execution works (test 2-3 simultaneous calls)
- [ ] **PHASE 0 BLOCKER**: Confirm Edison SDK version and installation method
- [ ] Document source of "79.4% accuracy" claim with full benchmark details
- [ ] Verify LITERATURE includes preprints (arXiv, bioRxiv) or document as exclusion
- [ ] Recruit and confirm expert reviewers BEFORE pilot start
- [ ] Test PRECEDENT search scope with known query, document actual databases
- [ ] Check E. coli dataset size against 5GB ANALYSIS limit
- [ ] Create detailed folder structure spec with file naming conventions
- [ ] Get API rate limits and monitoring strategy from Edison/FutureHouse
- [ ] Add "Tool Verification" section to Phase 0 plan: smoke test each claimed capability

## Overall Risk Assessment

**Execution Risk:** **High** - Multiple unverified assumptions about tool capabilities and API behavior
**Scientific Validity Risk:** Medium - Ground truth curation process undefined but fixable
**Timeline Risk:** **High** - Parallel execution failure or API rate limits could double timeline
**Budget Risk:** Medium - $200/run may be average; MOLECULES may cost more

## Verdict

**NO-GO (Until Blockers Resolved)**

**Justification:** Too many critical unknowns about tool capabilities and API behavior. The document assumes tools work as advertised without verification, which is dangerous for a time-constrained pilot. The "NO-GO" is temporary - can become GO WITH CONDITIONS after resolving blockers.

**Required before GO:**
1. Run Phase 0 API smoke tests to verify basic connectivity, parallel execution, and job submission
2. Document actual tool versions and API stability policy
3. Confirm expert reviewers recruited and available
4. Verify preprint coverage or adjust ground truth expectations

**After resolving blockers, verdict becomes: GO WITH CONDITIONS**
- Condition: Have sequential fallback plan if parallel execution fails
- Condition: Budget contingency for job failures/retries
- Condition: Document all tool limitations discovered in Phase 0/1 for final report

**Recommendation:** Expand Phase 0 to include systematic tool capability verification, not just API connectivity. Current Phase 0 is too minimal.
