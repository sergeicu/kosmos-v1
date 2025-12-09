# Phase 1: Job Type Smoke Tests

## Objective
Verify that all 4 Kosmos job types (LITERATURE, ANALYSIS, PRECEDENT, MOLECULES) can be invoked via the Edison API using TDD methodology.

## Prerequisites
- ✓ Phase 0 complete (API connectivity working)
- ✓ Edison SDK installed and documented
- ✓ API key configured in `.env`

---

## TDD Rules (MANDATORY)

1. **Write test first** - No implementation before test
2. **Watch it fail** - Confirm failure reason
3. **Minimal implementation** - Simplest code to pass
4. **Verify green** - All tests pass
5. **Refactor** - Clean up while staying green

---

## Your Task

### Step 1: Setup

```bash
cd tasks/s20251206_phase1_smoke_tests

# Copy working client from Phase 0 (if needed)
cp ../s20251206_phase0_api_test/src/phase0_test_api.py src/client_base.py
```

### Step 2: Write Test 1 - LITERATURE Job (RED)

**File:** `src/phase1_test_jobs.py`

```python
import pytest
import os
from dotenv import load_dotenv

load_dotenv()

def test_literature_job_submits():
    """Can we submit a LITERATURE job?"""
    from edison_client import Client, JobNames  # Adjust import based on Phase 0

    client = Client(api_key=os.getenv("EDISON_API_KEY"))

    try:
        # Minimal LITERATURE query
        job = client.submit_job(
            job_type=JobNames.LITERATURE,
            query="What is CRISPR-Cas9?",
            timeout=60  # Don't wait for completion, just submission
        )

        # Verify job was accepted
        assert job is not None, "Job submission returned None"
        assert hasattr(job, 'job_id') or 'job_id' in job, "No job_id in response"

        job_id = job.job_id if hasattr(job, 'job_id') else job['job_id']
        assert job_id is not None and len(str(job_id)) > 0, "job_id is empty"

        print(f"✓ LITERATURE job submitted: {job_id}")

    except Exception as e:
        pytest.fail(f"LITERATURE job submission failed: {e}")
```

**Run test:**
```bash
pytest src/phase1_test_jobs.py::test_literature_job_submits -v
```

**Expected failure modes:**
- `ImportError: cannot import name 'JobNames'` → Find correct enum/constant
- `TypeError: submit_job() got unexpected keyword` → Check method signature
- `API error: invalid job_type` → Check correct job type name

---

### Step 3: Implement Test 1 (GREEN)

**Research job submission API:**
- Check Edison SDK docs or cookbook examples
- Find correct method: `submit_job()`, `create_job()`, `run()`?
- Find correct job type identifier: `JobNames.LITERATURE`, `"literature"`, `"LITERATURE"`?

**Adjust code:**
```python
# Example adjustments based on actual SDK:
job = client.submit_literature_query(query="...")
# OR
job = client.submit_job(job_type="LITERATURE", query="...")
# OR
job = client.run(task="LITERATURE", prompt="...")
```

**Re-run test:**
```bash
pytest src/phase1_test_jobs.py::test_literature_job_submits -v
```

**Expected:** ✓ PASSED

**Save job_id to:** `output/phase1_results/submitted_jobs.txt`

---

### Step 4: Write Test 2 - ANALYSIS Job (RED)

**Add to:** `src/phase1_test_jobs.py`

```python
def test_analysis_job_submits():
    """Can we submit an ANALYSIS job?"""
    from edison_client import Client, JobNames
    import os

    client = Client(api_key=os.getenv("EDISON_API_KEY"))

    # Create minimal test data
    test_data_path = "input/test_data.csv"
    with open(test_data_path, 'w') as f:
        f.write("gene,sample1,sample2\n")
        f.write("GAPDH,100,120\n")
        f.write("ACTB,150,140\n")

    try:
        # Upload data (if required)
        # data_ref = client.upload_file(test_data_path)

        job = client.submit_job(
            job_type=JobNames.ANALYSIS,
            query="Describe this dataset",
            data_path=test_data_path
            # OR data_ref=data_ref
        )

        assert job is not None
        job_id = job.job_id if hasattr(job, 'job_id') else job['job_id']
        assert job_id is not None

        print(f"✓ ANALYSIS job submitted: {job_id}")

    except Exception as e:
        pytest.fail(f"ANALYSIS job submission failed: {e}")
```

**Run test:**
```bash
pytest src/phase1_test_jobs.py::test_analysis_job_submits -v
```

**Expected failures:**
- Data upload method unknown
- File format not accepted
- Job type name incorrect

---

### Step 5: Implement Test 2 (GREEN)

**Research data upload:**
- Check cookbook: https://edisonscientific.gitbook.io/edison-cookbook/edison-client/docs/edison_analysis_tutorial
- Find: `astore_file_content()`, `upload_data()`, or similar
- Determine if data path or data reference needed

**Adjust code:**
```python
# If file upload needed:
from edison_client import astore_file_content
data_ref = astore_file_content(test_data_path)

job = client.submit_job(
    job_type="ANALYSIS",
    query="Describe this dataset",
    data=data_ref  # or files=[data_ref]
)
```

**Re-run test:**
```bash
pytest src/phase1_test_jobs.py::test_analysis_job_submits -v
```

**Expected:** ✓ PASSED

---

### Step 6: Write Test 3 - PRECEDENT Job (RED)

**Add to:** `src/phase1_test_jobs.py`

```python
def test_precedent_job_submits():
    """Can we submit a PRECEDENT job?"""
    from edison_client import Client, JobNames
    import os

    client = Client(api_key=os.getenv("EDISON_API_KEY"))

    try:
        job = client.submit_job(
            job_type=JobNames.PRECEDENT,
            query="Has anyone developed mRNA vaccines for cancer?"
        )

        assert job is not None
        job_id = job.job_id if hasattr(job, 'job_id') else job['job_id']
        assert job_id is not None

        print(f"✓ PRECEDENT job submitted: {job_id}")

    except Exception as e:
        pytest.fail(f"PRECEDENT job submission failed: {e}")
```

**Run test:** Watch it fail, then implement based on actual SDK.

---

### Step 7: Write Test 4 - MOLECULES Job (RED)

**Add to:** `src/phase1_test_jobs.py`

```python
def test_molecules_job_submits():
    """Can we submit a MOLECULES job?"""
    from edison_client import Client, JobNames
    import os

    client = Client(api_key=os.getenv("EDISON_API_KEY"))

    try:
        job = client.submit_job(
            job_type=JobNames.MOLECULES,
            query="Predict ADMET properties for aspirin (SMILES: CC(=O)Oc1ccccc1C(=O)O)"
        )

        assert job is not None
        job_id = job.job_id if hasattr(job, 'job_id') else job['job_id']
        assert job_id is not None

        print(f"✓ MOLECULES job submitted: {job_id}")

    except Exception as e:
        pytest.fail(f"MOLECULES job submission failed: {e}")
```

**Run test:** Watch it fail, then implement.

---

### Step 8: Implement Tests 3 & 4 (GREEN)

Adjust based on actual SDK patterns discovered in Tests 1-2.

**Re-run full suite:**
```bash
pytest src/phase1_test_jobs.py -v
```

**Expected:** 4/4 PASSED

---

### Step 9: Create Reusable Client Wrapper

**File:** `src/edison_wrapper.py`

Extract common patterns:

```python
"""Reusable Edison client wrapper for Kosmos experiments."""
import os
from dotenv import load_dotenv
from edison_client import Client, JobNames  # Adjust imports

load_dotenv()

class KosmosClient:
    """Wrapper for Edison API with Kosmos-specific methods."""

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("EDISON_API_KEY")
        self.client = Client(api_key=self.api_key)

    def submit_literature(self, query):
        """Submit LITERATURE job."""
        return self.client.submit_job(
            job_type=JobNames.LITERATURE,
            query=query
        )

    def submit_analysis(self, query, data_path):
        """Submit ANALYSIS job with data."""
        # Adjust based on actual API
        return self.client.submit_job(
            job_type=JobNames.ANALYSIS,
            query=query,
            data_path=data_path
        )

    def submit_precedent(self, query):
        """Submit PRECEDENT job."""
        return self.client.submit_job(
            job_type=JobNames.PRECEDENT,
            query=query
        )

    def submit_molecules(self, query):
        """Submit MOLECULES job."""
        return self.client.submit_job(
            job_type=JobNames.MOLECULES,
            query=query
        )

    def get_job_status(self, job_id):
        """Check job status."""
        return self.client.get_status(job_id)

    def get_job_result(self, job_id):
        """Retrieve completed job result."""
        return self.client.get_result(job_id)
```

**Test wrapper:**
```bash
pytest src/phase1_test_jobs.py -v  # Should still pass with wrapper
```

---

### Step 10: Generate Report

**Create:** `output/phase1_results/phase1_report.md`

```markdown
# Phase 1: Job Type Smoke Tests - Results

## Execution Summary
- **Date:** {timestamp}
- **Duration:** {X minutes}
- **All tests passed:** ✓ / ✗

## Job Submission Results

### LITERATURE Job
- **Status:** PASSED ✓
- **Job ID:** {job_id}
- **Method:** `client.submit_job(job_type="LITERATURE", ...)`
- **Response time:** {X seconds}

### ANALYSIS Job
- **Status:** PASSED ✓
- **Job ID:** {job_id}
- **Data upload:** {Required / Not required}
- **Method:** `{actual method signature}`

### PRECEDENT Job
- **Status:** PASSED ✓
- **Job ID:** {job_id}
- **Method:** `{actual method}`

### MOLECULES Job
- **Status:** PASSED ✓
- **Job ID:** {job_id}
- **Method:** `{actual method}`

## API Patterns Discovered

**Job submission signature:**
```python
client.submit_job(
    job_type={str or enum},
    query={str},
    data_path={optional str},
    ...
)
```

**Response format:**
```python
{
    "job_id": "abc123",
    "status": "pending",
    ...
}
```

**Job type identifiers:**
- LITERATURE: `{actual value}`
- ANALYSIS: `{actual value}`
- PRECEDENT: `{actual value}`
- MOLECULES: `{actual value}`

## Reusable Components

Created: `src/edison_wrapper.py`
- Encapsulates job submission for all 4 types
- Handles authentication
- Ready for use in Phase 2 experiments

## Blocking Issues
{None or list}

## Next Steps
- [ ] Copy `edison_wrapper.py` to each experiment directory
- [ ] Proceed to Phase 2 (benchmark experiments)
- [ ] Monitor submitted jobs (may still be running)

## Submitted Jobs Log
{List all job IDs for monitoring}

## Raw Logs
See: `../logs/phase1_execution.log`
```

---

### Step 11: Monitor Jobs (Optional)

Jobs may still be running. Create monitoring script:

**File:** `src/monitor_jobs.py`

```python
"""Monitor status of submitted smoke test jobs."""
from edison_wrapper import KosmosClient
import json

client = KosmosClient()

# Read job IDs from test output
with open("output/phase1_results/submitted_jobs.txt") as f:
    job_ids = [line.strip() for line in f if line.strip()]

for job_id in job_ids:
    try:
        status = client.get_job_status(job_id)
        print(f"{job_id}: {status}")
    except Exception as e:
        print(f"{job_id}: Error - {e}")
```

**Run:**
```bash
python src/monitor_jobs.py
```

---

## Success Criteria

- [ ] All 4 tests written BEFORE implementation
- [ ] All 4 tests failed initially (RED)
- [ ] All 4 tests pass after implementation (GREEN)
- [ ] `pytest src/phase1_test_jobs.py -v` shows 4/4 passed
- [ ] Reusable wrapper created (`edison_wrapper.py`)
- [ ] Report generated
- [ ] Job IDs logged for monitoring

---

## Failure Modes & Solutions

### Job Type Not Supported
- **Problem:** API returns "unknown job type"
- **Solutions:**
  1. Check Edison documentation for correct names
  2. May be regional names ("LITERATURE" vs "PaperQA")
  3. Some job types may require special access

### Data Upload Fails (ANALYSIS)
- **Problem:** Can't upload CSV file
- **Solutions:**
  1. Check file size limits (5GB uncompressed?)
  2. Check format requirements (CSV vs. TSV vs. JSON)
  3. Use `astore_file_content()` from cookbook

### Rate Limiting
- **Problem:** 429 Too Many Requests
- **Solutions:**
  1. Add 5-second delay between job submissions
  2. Submit sequentially, not in parallel
  3. Check rate limits in API docs

### Job Submission Succeeds but Jobs Fail
- **Problem:** All jobs return error status
- **Solutions:**
  1. Check query format (some may need specific structure)
  2. Verify account has quota/credits
  3. Test queries may be too trivial (use domain-specific examples)

---

## File Naming Convention

- Tests: `src/phase1_*.py`
- Wrapper: `src/edison_wrapper.py`
- Logs: `logs/phase1_execution.log`
- Outputs: `output/phase1_results/*`

---

## Budget

**Time:** 30 minutes
**Cost:** $0-800 (jobs submitted but may not need to wait for completion)
- Note: If jobs run to completion, may cost ~$200 each
- Recommendation: Don't wait for results, just verify submission works

---

## Important Notes

1. **Don't wait for jobs to complete** - This phase tests submission, not execution
2. **Document all patterns** - Future experiments will reuse this
3. **Job IDs are valuable** - Save them for later inspection
4. **Wrapper is critical** - Will save hours in Phase 2

---

## Ready for Phase 2?

You're ready when:
- [ ] All 4 job types submit successfully
- [ ] Wrapper class works
- [ ] No blocking API issues
- [ ] Documentation complete

**If any test fails:** Fix before Phase 2. Experiments can't run without working job submission.
