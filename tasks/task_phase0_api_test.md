# Phase 0: Edison API Connectivity Test

## Objective
Validate that Edison API access works using Test-Driven Development (TDD). Write tests first, watch them fail, then implement minimal code to make them pass.

## Context
This is Phase 0 of the Kosmos pilot. You MUST establish working API connectivity before any experiments can run. This task follows strict TDD methodology.

---

## TDD Rules (MANDATORY)

1. **Write test first** - No implementation code before test exists
2. **Watch it fail** - Run test, confirm it fails for the RIGHT reason
3. **Minimal implementation** - Write simplest code to pass
4. **Verify green** - Run test, confirm it passes
5. **Refactor if needed** - Clean up while keeping tests green

**If you write implementation before tests: DELETE IT and start over.**

---

## Your Task

### Step 1: Setup Environment

```bash
# Working directory
cd tasks/s20251206_phase0_api_test

# Install dependencies (if needed)
pip install pytest requests python-dotenv

# Create .env file for API key
cat > .env << EOF
EDISON_API_KEY=your_key_here
EOF
```

### Step 2: Write Test 1 - Import Client (RED)

**File:** `src/phase0_test_api.py`

```python
import pytest

def test_import_edison_client():
    """Can we import the Edison SDK?"""
    try:
        from edison_client import Client
        assert Client is not None
    except ImportError as e:
        pytest.fail(f"Failed to import Edison client: {e}")
```

**Run test:**
```bash
pytest src/phase0_test_api.py::test_import_edison_client -v
```

**Expected output:** `ImportError: No module named 'edison_client'` ✓ (correct failure)

**If test passes:** You already have the SDK. Document version in `logs/phase0_execution.log`

---

### Step 3: Implement Test 1 (GREEN)

**Research Edison SDK:**
- Check if package name is `edison-client`, `edison_scientific`, or similar
- Check FutureHouse GitHub: https://github.com/Future-House
- Check pip: `pip search edison` or `pip search futureHouse`
- Check cookbook examples for import statements

**Install:**
```bash
# Try these in order:
pip install edison-client
# OR
pip install edison-scientific
# OR
git clone https://github.com/Future-House/edison-client.git && pip install -e edison-client/
```

**Re-run test:**
```bash
pytest src/phase0_test_api.py::test_import_edison_client -v
```

**Expected:** ✓ PASSED (green)

**Document in:** `logs/phase0_execution.log`
- Package name
- Installation method
- Version number

---

### Step 4: Write Test 2 - Authentication (RED)

**Add to:** `src/phase0_test_api.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

def test_authenticate():
    """Can we authenticate with API key?"""
    from edison_client import Client

    api_key = os.getenv("EDISON_API_KEY")
    assert api_key is not None, "EDISON_API_KEY not set in .env file"
    assert len(api_key) > 10, "API key seems invalid (too short)"

    try:
        client = Client(api_key=api_key)
        # Method name depends on SDK - try these:
        # client.authenticate()
        # client.verify_credentials()
        # Or just creating client is enough
        assert client is not None
    except Exception as e:
        pytest.fail(f"Authentication failed: {e}")
```

**Run test:**
```bash
pytest src/phase0_test_api.py::test_authenticate -v
```

**Expected failures:**
- `EDISON_API_KEY not set` → Go get API key
- `Client() takes different arguments` → Check SDK docs
- `Authentication error` → Check API key validity

---

### Step 5: Implement Test 2 (GREEN)

**Get API key:**
1. Check grant documentation for API access
2. Contact FutureHouse/Edison Scientific
3. Check if there's a sandbox/demo key
4. Add to `.env` file

**Fix client initialization:**
```python
# Adjust based on actual SDK signature
client = Client(api_key=api_key)
# OR
client = Client(token=api_key)
# OR
client = Client()  # Reads from environment automatically
```

**Re-run test:**
```bash
pytest src/phase0_test_api.py::test_authenticate -v
```

**Expected:** ✓ PASSED

---

### Step 6: Write Test 3 - Basic Query (RED)

**Add to:** `src/phase0_test_api.py`

```python
def test_basic_query():
    """Can we make a simple API call?"""
    from edison_client import Client
    import os

    client = Client(api_key=os.getenv("EDISON_API_KEY"))

    try:
        # Try health check endpoint (adjust based on SDK)
        response = client.ping()
        # OR
        # response = client.health()
        # OR
        # response = client.get_status()

        assert response is not None
        # Check response format
        assert hasattr(response, 'status') or isinstance(response, dict)

    except Exception as e:
        pytest.fail(f"Basic query failed: {e}")
```

**Run test:**
```bash
pytest src/phase0_test_api.py::test_basic_query -v
```

**Expected failures:**
- `AttributeError: 'Client' object has no attribute 'ping'` → Find correct method
- `API error: 401` → Authentication issue
- `API error: 429` → Rate limit (wait and retry)

---

### Step 7: Implement Test 3 (GREEN)

**Find health check method:**
- Check SDK documentation
- Try `dir(client)` to list methods
- Look for: `ping()`, `health()`, `status()`, `verify()`
- If none exist, submit minimal job instead:

```python
# Fallback: minimal LITERATURE query
response = client.submit_job(
    job_type="LITERATURE",
    query="What is CRISPR?"
)
assert response.job_id is not None
```

**Re-run test:**
```bash
pytest src/phase0_test_api.py::test_basic_query -v
```

**Expected:** ✓ PASSED

---

### Step 8: Run Full Test Suite

```bash
pytest src/phase0_test_api.py -v
```

**Expected output:**
```
test_import_edison_client PASSED
test_authenticate PASSED
test_basic_query PASSED

========================= 3 passed in X.XXs =========================
```

---

### Step 9: Generate Report

**Create:** `output/phase0_results/phase0_report.md`

```markdown
# Phase 0: API Connectivity Test - Results

## Execution Summary
- **Date:** {timestamp}
- **Duration:** {X minutes}
- **All tests passed:** ✓ / ✗

## Environment
- **Python version:** {3.x.x}
- **Edison SDK:** {package name} v{version}
- **Installation method:** {pip / git / manual}

## Test Results

### Test 1: Import Client
- **Status:** PASSED ✓
- **Package:** {edison_client or actual name}
- **Import path:** `from {package} import {Class}`

### Test 2: Authentication
- **Status:** PASSED ✓
- **API key source:** {.env file}
- **Client initialization:** `Client(api_key=...)`
- **Notes:** {any authentication quirks}

### Test 3: Basic Query
- **Status:** PASSED ✓
- **Method used:** {ping() or health() or submit_job()}
- **Response format:** {dict / object / other}
- **Latency:** {X seconds}

## Blocking Issues (if any)
{None or list issues}

## Next Steps
- [ ] Proceed to Phase 1 (job type smoke tests)
- [ ] Document SDK quirks for other developers
- [ ] Share API key securely with team

## Raw Logs
See: `../logs/phase0_execution.log`

## Code Artifacts
- Test file: `src/phase0_test_api.py`
- Client wrapper (if created): `src/edison_client_wrapper.py`
```

---

### Step 10: Save Execution Log

**Create:** `logs/phase0_execution.log`

Include:
- Full pytest output
- Any error messages encountered
- SDK installation steps
- Environment variables used (REDACT api key!)
- Timestamps

---

## Success Criteria

- [ ] All 3 tests written BEFORE implementation
- [ ] All 3 tests failed initially (RED)
- [ ] All 3 tests pass after implementation (GREEN)
- [ ] Report generated
- [ ] Edison SDK documented (package name, version)
- [ ] API key stored securely (.env, not committed to git)

---

## If Tests Fail

### Import Error
- **Problem:** Can't find Edison SDK
- **Solutions:**
  1. Check FutureHouse GitHub for package
  2. Contact Edison Scientific for SDK access
  3. Check if it's a private package (requires credentials)
  4. Use cookbook examples to reverse-engineer import

### Authentication Error
- **Problem:** API key invalid or expired
- **Solutions:**
  1. Verify API key copied correctly (no extra spaces)
  2. Check if key needs activation
  3. Request new key from grant administrator
  4. Check if IP allowlist required

### API Error (500, 503)
- **Problem:** Edison API down
- **Solutions:**
  1. Check status page: https://status.edisonscientific.com (if exists)
  2. Wait 10 minutes, retry
  3. Contact Edison support
  4. Document in logs, escalate to PI

### Rate Limit (429)
- **Problem:** Too many requests
- **Solutions:**
  1. Wait 60 seconds between retries
  2. Check if free tier has limits
  3. Verify only one test instance running
  4. Document rate limits for Phase 2 planning

---

## File Naming Convention

- Tests: `src/phase0_*.py`
- Logs: `logs/phase0_execution.log`
- Outputs: `output/phase0_results/*`
- Environment: `.env` (DO NOT COMMIT)

---

## Acceptance Criteria

This phase is complete when:
- [ ] `pytest src/phase0_test_api.py -v` shows 3/3 passed
- [ ] Report generated with all sections filled
- [ ] SDK package and version documented
- [ ] API key stored securely
- [ ] Logs capture full execution trace
- [ ] No blocking issues preventing Phase 1

---

## Budget

**Time:** 30 minutes
**Cost:** $0 (no Kosmos jobs submitted, just health checks)

---

## Tools Available

- pytest (test framework)
- python-dotenv (environment variables)
- requests (HTTP if needed for API debugging)
- Standard Python libraries

---

## Important Notes

1. **DO NOT commit .env file** - Add to .gitignore
2. **Follow TDD strictly** - Write test → Watch fail → Implement → Watch pass
3. **Document everything** - Future developers will thank you
4. **Minimal implementation** - Don't over-engineer; just make tests pass
5. **If stuck >30 min** - Document blockers and escalate

---

## Red Flags

**You're doing it wrong if:**
- You wrote implementation before tests
- Tests passed immediately (didn't see them fail)
- You skipped a test because "it's obvious"
- You're trying to make the code "perfect"
- You've spent >1 hour on this phase

**Fix:** Go back, delete implementation, start with RED test first.
