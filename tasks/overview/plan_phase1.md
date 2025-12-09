# Phase 1 Implementation Plan: Kosmos API Testing

## Objective
Establish working Edison API integration using Test-Driven Development (TDD) methodology across Phase 0 (connectivity) and Phase 1 (job type smoke tests).

---

## Phase 0: API Connectivity Tests

### Test 1: Import Edison Client

**File:** `tasks/s20251206_phase0_api_test/src/phase0_test_api.py`

**RED - Write failing test:**
```python
import pytest

def test_import_edison_client():
    """Can we import the Edison SDK?"""
    try:
        from edison_client import Client
        assert Client is not None
    except ImportError as e:
        pytest.fail(f"Failed to import: {e}")
```

**Run test:** `pytest tasks/s20251206_phase0_api_test/src/phase0_test_api.py -v`
**Expected:** `ImportError: No module named 'edison_client'`

**GREEN - Minimal implementation:**
- Research Edison SDK installation
- Install via pip: `pip install edison-client` (or equivalent)
- Re-run test until passes

**REFACTOR:** Document installation in README

---

### Test 2: Authentication

**RED - Write failing test:**
```python
import os

def test_authenticate():
    """Can we authenticate with API key?"""
    from edison_client import Client

    api_key = os.getenv("EDISON_API_KEY")
    assert api_key is not None, "EDISON_API_KEY not set in environment"

    client = Client(api_key=api_key)
    # Assuming SDK has an auth check method
    assert client.is_authenticated() or client.auth_status == "valid"
```

**Run test:** Expect failure (no API key in environment or auth fails)

**GREEN - Minimal implementation:**
- Obtain API key from Edison Scientific
- Set environment variable: `export EDISON_API_KEY=your_key`
- Re-run test

**REFACTOR:** Add `.env` file support, document in README

---

### Test 3: Basic Query

**RED - Write failing test:**
```python
def test_basic_health_check():
    """Can we make a simple API call?"""
    from edison_client import Client
    import os

    client = Client(api_key=os.getenv("EDISON_API_KEY"))

    # Minimal query to test connectivity
    # Actual method depends on SDK docs
    response = client.ping()  # or client.get_status() or similar
    assert response.status_code == 200 or response.status == "ok"
```

**Run test:** Expect failure (method doesn't exist or API unreachable)

**GREEN - Minimal implementation:**
- Read Edison SDK documentation to find health check method
- If no health check exists, use minimal LITERATURE query
- Implement retry logic if needed
- Re-run test

**REFACTOR:** Extract client initialization into fixture

---

## Phase 1: Job Type Smoke Tests

### Test 4: LITERATURE Job Callable

**RED - Write failing test:**
```python
def test_literature_job_submits():
    """Can we submit a LITERATURE job?"""
    from edison_client import Client, JobNames
    import os

    client = Client(api_key=os.getenv("EDISON_API_KEY"))

    job = client.submit_job(
        job_type=JobNames.LITERATURE,
        query="What is CRISPR-Cas9?"
    )

    assert job is not None
    assert hasattr(job, 'job_id')
    assert job.job_id is not None
```

**Run test:** Expect failure (method signature wrong, JobNames doesn't exist, etc.)

**GREEN - Minimal implementation:**
- Read Edison SDK docs for job submission API
- Adjust method call to match actual SDK
- Handle response parsing
- Re-run test

**REFACTOR:** Extract job submission into helper function

---

### Test 5: ANALYSIS Job Callable

**RED - Write failing test:**
```python
def test_analysis_job_submits():
    """Can we submit an ANALYSIS job?"""
    from edison_client import Client, JobNames
    import os

    client = Client(api_key=os.getenv("EDISON_API_KEY"))

    # Minimal test data (empty CSV or simple array)
    test_data_path = "tasks/s20251206_phase1_smoke_tests/input/test_data.csv"

    job = client.submit_job(
        job_type=JobNames.ANALYSIS,
        query="Describe this dataset",
        data_path=test_data_path
    )

    assert job is not None
    assert job.job_id is not None
```

**Run test:** Expect failure (data upload API unknown, etc.)

**GREEN - Minimal implementation:**
- Create minimal test CSV (2 rows, 3 columns)
- Research data upload API
- Implement upload + job submission
- Re-run test

**REFACTOR:** Parameterize test for different data formats

---

### Test 6: PRECEDENT Job Callable

**RED - Write failing test:**
```python
def test_precedent_job_submits():
    """Can we submit a PRECEDENT job?"""
    from edison_client import Client, JobNames
    import os

    client = Client(api_key=os.getenv("EDISON_API_KEY"))

    job = client.submit_job(
        job_type=JobNames.PRECEDENT,
        query="Has anyone developed mRNA vaccines for cancer?"
    )

    assert job is not None
    assert job.job_id is not None
```

**Run test:** Expect failure initially

**GREEN - Minimal implementation:**
- Adjust for PRECEDENT-specific API parameters
- Re-run test

---

### Test 7: MOLECULES Job Callable

**RED - Write failing test:**
```python
def test_molecules_job_submits():
    """Can we submit a MOLECULES job?"""
    from edison_client import Client, JobNames
    import os

    client = Client(api_key=os.getenv("EDISON_API_KEY"))

    job = client.submit_job(
        job_type=JobNames.MOLECULES,
        query="Predict ADMET properties for aspirin (SMILES: CC(=O)Oc1ccccc1C(=O)O)"
    )

    assert job is not None
    assert job.job_id is not None
```

**Run test:** Expect failure initially

**GREEN - Minimal implementation:**
- Handle SMILES input format
- Re-run test

---

## Test Execution Checklist

**Before writing any implementation code:**
- [ ] Write all 7 tests
- [ ] Run full test suite: `pytest tasks/s20251206_phase*/src/ -v`
- [ ] Confirm ALL tests fail (not error due to syntax)
- [ ] Document expected failure modes

**Implementation order (TDD cycle for each):**
1. [ ] Test 1: Import → Implement → Green
2. [ ] Test 2: Auth → Implement → Green
3. [ ] Test 3: Health check → Implement → Green
4. [ ] Test 4: LITERATURE → Implement → Green
5. [ ] Test 5: ANALYSIS → Implement → Green
6. [ ] Test 6: PRECEDENT → Implement → Green
7. [ ] Test 7: MOLECULES → Implement → Green

**Verification:**
- [ ] Run `pytest tasks/s20251206_phase*/src/ -v` → All green
- [ ] No skipped tests
- [ ] No warnings
- [ ] Logs saved to `logs/phase0_execution.log` and `logs/phase1_execution.log`

---

## Output Structure

### Phase 0 Outputs
**Directory:** `tasks/s20251206_phase0_api_test/output/phase0_results/`

**Files:**
- `api_test_results.json` - Test pass/fail status
- `connection_log.txt` - Raw API responses
- `phase0_report.md` - Human-readable summary

### Phase 1 Outputs
**Directory:** `tasks/s20251206_phase1_smoke_tests/output/phase1_results/`

**Files:**
- `job_submission_results.json` - All 4 job submissions
- `job_ids.txt` - Submitted job IDs for monitoring
- `phase1_report.md` - Summary of callable vs. failed jobs

---

## Success Criteria

**Phase 0 Complete:**
- All 3 API tests pass
- Documentation exists for setup
- API key management secure

**Phase 1 Complete:**
- All 4 job type tests pass (jobs submit successfully)
- Job IDs returned for each type
- No authentication errors

**Ready for Phase 2:**
- Reusable client wrapper exists
- Job submission parameterized by type
- Test fixtures available for Phase 2 experiments

---

## Blocking Issues Resolution

| Issue | Resolution Path |
|-------|----------------|
| **No Edison SDK docs** | 1. Search GitHub for edison-client<br>2. Contact FutureHouse directly<br>3. Reverse-engineer from cookbook examples |
| **API key unavailable** | 1. Check grant budget for API access<br>2. Request from PI/collaborator<br>3. Use sandbox/demo environment if available |
| **Job submission fails** | 1. Check cookbook for working examples<br>2. Validate input format (JSON schema)<br>3. Test with minimal queries first |

---

## Next Steps After Phase 1

Once all tests green:
1. **Extract reusable components:**
   - Client initialization fixture
   - Job submission wrapper
   - Response parsing utilities

2. **Prepare for Phase 2:**
   - Identify ground truth datasets
   - Write Phase 2 test suite
   - Create task prompt files for parallel execution

3. **Document learnings:**
   - API quirks discovered
   - Rate limits observed
   - Optimal query patterns
