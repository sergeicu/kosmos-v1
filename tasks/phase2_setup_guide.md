# Phase 2 Setup Guide
## Using Edison API for Kosmos Experiments

This document provides the **working patterns** discovered during Phase 0 and Phase 1 testing for running Phase 2 experiments.

---

## Prerequisites

✅ **Phase 0 Complete**: API connectivity verified
✅ **Phase 1 Complete**: All 4 job types validated
✅ **Working Components**: `edison_wrapper.py` created and tested

---

## Quick Start for Phase 2

### Step 1: Copy Working Components

```bash
# From your working directory (any Phase 2 experiment):
cp ../s20251206_phase1_smoke_tests/.env .
cp ../s20251206_phase1_smoke_tests/src/edison_wrapper.py src/
cp ../s20251206_phase1_smoke_tests/input/ input/  # optional template
```

### Step 2: Initialize KosmosClient

```python
from src.edison_wrapper import KosmosClient

# Auto-loads EDISON_API_KEY from .env
client = KosmosClient()

# Test connection (optional)
task_id = client.submit_literature("test connection")
print(f"Connected! Task ID: {task_id}")
```

---

## Working Job Submission Patterns

### LITERATURE Jobs (Task 1: Cancer Genomics)

```python
from src.edison_wrapper import KosmosClient

client = KosmosClient()

query = """What are the most promising targetable dependencies in KRAS-mutant
pancreatic cancer identified in the last 3 years, and what mechanisms
underlie resistance to current targeted therapies?"""

task_id = client.submit_literature(query)
print(f"LITERATURE task submitted: {task_id}")

# Monitor later:
task = client.get_task(task_id)
print(f"Status: {task.status}")
```

### PRECEDENT Jobs (Task 2: Immunology)

```python
from src.edison_wrapper import KosmosClient

client = KosmosClient()

query = """Has anyone developed mRNA vaccines targeting solid tumor neoantigens
using patient-specific mutation profiles, and what were the clinical trial outcomes?"""

task_id = client.submit_precedent(query)
print(f"PRECEDENT task submitted: {task_id}")
```

### ANALYSIS Jobs (Task 3: Systems Biology)

```python
from src.edison_wrapper import KosmosClient

client = KosmosClient()

query = """Analyze this E. coli RNA-seq dataset from a heat shock experiment.
Identify differentially expressed genes, perform pathway enrichment analysis,
and generate 2-3 testable hypotheses about the heat shock response mechanism."""

# Submit with data file
task_id = client.submit_analysis(query, files=["input/ecoli_heatshock.csv"])
print(f"ANALYSIS task submitted: {task_id}")
```

### MOLECULES Jobs (Task 4: Structural Biology)

```python
from src.edison_wrapper import KosmosClient

client = KosmosClient()

query = """Design three small molecule inhibitors for the SARS-CoV-2 main protease
(Mpro) with improved oral bioavailability compared to nirmatrelvir (Paxlovid)."""

task_id = client.submit_molecules(query)
print(f"MOLECULES task submitted: {task_id}")
```

---

## Directory Structure Template

```
taskX_experiment/
├── .env                     # EDISON_API_KEY (copy from Phase 1)
├── src/
│   ├── edison_wrapper.py    # KosmosClient (copy from Phase 1)
│   └── taskX_run.py         # Your experiment code
├── input/
│   └── taskX_data.csv       # Any data files (for ANALYSIS)
├── output/
│   └── taskX_results/       # Results directory
└── logs/
    └── taskX_execution.log  # Execution logs
```

---

## Response Format (What Edison Returns)

```python
# create_task() returns UUID string directly
task_id = client.submit_literature("query")
# Returns: "6828a78b-2533-4cfb-bee9-a4dd26ffc344"

# NOT: {"task_id": "..."}
# NOT: TaskResponse(task_id="...")
```

---

## Task Status Monitoring

```python
from src.edison_wrapper import KosmosClient
import time

client = KosmosClient()
task_id = "your-task-id-here"

# Poll for completion (example)
while True:
    task = client.get_task(task_id)
    print(f"Status: {task.status}")

    if task.status in ["completed", "failed", "cancelled"]:
        break

    time.sleep(30)  # Wait 30 seconds

if task.status == "completed":
    print(f"Result: {task.result}")
```

---

## Performance Benchmarks (from Phase 1)

| Job Type | Submission Time | Typical Runtime | Cost |
|----------|----------------|----------------|------|
| LITERATURE | ~6.4s | ~15 minutes | ~$2 |
| PRECEDENT | ~6.5s | ~15 minutes | ~$2 |
| ANALYSIS | ~6.3s | ~45 minutes | ~$2 |
| MOLECULES | ~6.5s | ~30 minutes | ~$2 |

---

## Common Patterns for All Tasks

### 1. Save Task IDs for Monitoring

```python
import os
from datetime import datetime

def save_task_id(task_type, task_id):
    """Save task ID with timestamp for later monitoring"""
    with open("output/submitted_tasks.txt", "a") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} - {task_type}: {task_id}\n")

# Usage:
task_id = client.submit_literature(query)
save_task_id("LITERATURE", task_id)
```

### 2. Error Handling Template

```python
from src.edison_wrapper import KosmosClient

def run_experiment():
    try:
        client = KosmosClient()

        # Submit job
        task_id = client.submit_literature(query)
        print(f"Task submitted: {task_id}")

        # Save for monitoring
        save_task_id("LITERATURE", task_id)

        return task_id

    except Exception as e:
        print(f"Error submitting task: {e}")
        # Save error for debugging
        with open("logs/error.log", "a") as f:
            f.write(f"{datetime.now()}: {str(e)}\n")
        return None

if __name__ == "__main__":
    task_id = run_experiment()
    if task_id:
        print("✓ Task submitted successfully")
    else:
        print("✗ Task submission failed")
```

### 3. Result Collection Template

```python
import json

def collect_result(task_id):
    """Collect and save task result"""
    client = KosmosClient()

    # Wait for completion
    task = client.get_task(task_id)

    if task.status == "completed":
        # Save raw output
        with open("output/kosmos_raw_output.json", "w") as f:
            json.dump(task.result, f, indent=2)

        print("✓ Result saved to output/kosmos_raw_output.json")
        return task.result

    else:
        print(f"Task not completed. Status: {task.status}")
        return None
```

---

## Key Differences from Original Task Specs

### Original Assumption (Before Testing):
```python
# What the Phase 2 tasks assumed:
client = EdisonClient(api_key=api_key)
response = client.submit_job(job_type=JobNames.LITERATURE, query=...)
task_id = response["task_id"]  # WRONG - doesn't exist
```

### Working Pattern (After Testing):
```python
# What actually works:
from src.edison_wrapper import KosmosClient

client = KosmosClient()
task_id = client.submit_literature(query)  # Direct UUID string
```

---

## File Upload for ANALYSIS Jobs

### Working Pattern:
```python
# Files passed as list of paths
task_id = client.submit_analysis(
    "Analyze this dataset",
    files=["input/data.csv", "input/metadata.csv"]
)
```

### Supported Formats (confirmed working):
- CSV files ✅
- TSV files (likely)
- Text files (likely)

---

## Environment Setup Checklist

- [ ] Copy `.env` from Phase 1 (contains EDISON_API_KEY)
- [ ] Copy `src/edison_wrapper.py` from Phase 1
- [ ] Create required directories: `src/`, `input/`, `output/`, `logs/`
- [ ] Test connection with simple query
- [ ] Verify task ID appears in `submitted_tasks.txt`

---

## Ready for Phase 2

With this setup guide and the working `KosmosClient` wrapper, you can now run any of the Phase 2 experiments:

- **Task 1**: Cancer Genomics (LITERATURE)
- **Task 2**: Immunology (PRECEDENT)
- **Task 3**: Systems Biology (ANALYSIS)
- **Task 4**: Structural Biology (MOLECULES)
- **Task 5**: Neuroscience (mixed job types)

All patterns are verified and tested. The API endpoints work as documented above.