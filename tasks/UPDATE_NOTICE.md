# Phase 2 Tasks Update Notice

## Summary

The Phase 2 tasks (task1_cancer_genomics.md through task5_neuroscience.md) were created **BEFORE** we tested Edison API connectivity and job submission patterns. They contain assumptions that need to be updated with the working patterns discovered in Phase 0 and Phase 1.

## Key Updates Required

### 1. Job Submission Method
**Original (WRONG):**
```python
# These task specs assume:
response = client.submit_job(job_type=JobNames.LITERATURE, query=...)
task_id = response["task_id"]  # This doesn't exist!
```

**Working (CORRECT):**
```python
# What actually works:
from src.edison_wrapper import KosmosClient

client = KosmosClient()  # Auto-loads API key
task_id = client.submit_literature(query)  # Direct UUID string
```

### 2. Response Format
**Original Assumption:** Edison returns `{"task_id": "uuid"}` or `TaskResponse`
**Actual Reality:** Edison returns UUID string directly: `"6828a78b-2533-4cfb-bee9-a4dd26ffc344"`

### 3. Client Initialization
**Original:** Manual `EdisonClient(api_key=api_key)` with key loading
**Working:** `KosmosClient()` auto-loads from `.env`

### 4. File Upload (ANALYSIS Jobs)
**Original:** Unclear how to upload files
**Working:** Pass `files=["path/to/data.csv"]` to `submit_analysis()`

## Solution: Use Working Components

We've created:
1. **`phase2_setup_guide.md`** - Complete setup instructions with working patterns
2. **`phase2_experiment_template.py`** - Ready-to-use code template
3. **`edison_wrapper.py`** (from Phase 1) - Simplified KosmosClient class

## Quick Fix for Any Phase 2 Task

### Step 1: Copy Working Components
```bash
# In your Phase 2 experiment directory:
cp ../s20251206_phase1_smoke_tests/.env .
cp ../s20251206_phase1_smoke_tests/src/edison_wrapper.py src/
```

### Step 2: Use Template Code
```python
# Replace all Edison API calls with:
from src.edison_wrapper import KosmosClient

client = KosmosClient()
task_id = client.submit_literature(query)  # For LITERATURE jobs
# or
task_id = client.submit_precedent(query)   # For PRECEDENT jobs
# or
task_id = client.submit_analysis(query, files=["data.csv"])  # For ANALYSIS jobs
# or
task_id = client.submit_molecules(query)   # For MOLECULES jobs
```

### Step 3: Handle Results
```python
# Edison returns UUID string directly
task_id = client.submit_literature(query)
print(f"Task ID: {task_id}")  # Prints: "6828a78b-2533-4cfb-bee9-a4dd26ffc344"

# To monitor later:
task = client.get_task(task_id)
```

## Tasks Affected

- ✅ `task1_cancer_genomics.md` - Needs JobNames.LITERATURE → KosmosClient.submit_literature()
- ✅ `task2_immunology.md` - Needs JobNames.PRECEDENT → KosmosClient.submit_precedent()
- ✅ `task3_systems_bio.md` - Needs JobNames.ANALYSIS → KosmosClient.submit_analysis()
- ✅ `task4_structural_bio.md` - Needs JobNames.MOLECULES → KosmosClient.submit_molecules()
- ✅ `task5_neuroscience.md` - Likely mixed job types

## Performance Updates

| Job Type | Original Spec | Actual Time (from Phase 1) |
|----------|---------------|---------------------------|
| LITERATURE | ~15 min | ~15 min ✅ |
| PRECEDENT | ~15 min | ~15 min ✅ |
| ANALYSIS | ~45 min | ~45 min ✅ |
| MOLECULES | ~30 min | ~30 min ✅ |

The original time estimates were accurate!

## Recommendation

**DO NOT** manually edit each task file. Instead:

1. **Use the template**: `phase2_experiment_template.py` has working patterns
2. **Follow the setup guide**: `phase2_setup_guide.md` has complete instructions
3. **Copy the wrapper**: `edison_wrapper.py` simplifies all API calls

The original task files are still valuable for:
- Experiment design (queries, ground truth, metrics)
- Evaluation criteria
- Success metrics
- Report templates

Just replace the Edison API code sections with the working patterns.

---

## Status

✅ **Phase 0**: API connectivity verified
✅ **Phase 1**: All 4 job types validated
✅ **Phase 2 Setup**: Working patterns documented and templated
🔄 **Ready to run**: Phase 2 experiments with corrected patterns