#!/usr/bin/env python3
"""
Monitor Task 3 until completion and process results
"""

from edison_wrapper import KosmosClient
import json
import os
import time
from datetime import datetime

client = KosmosClient()

# Read the task ID
with open("output/task3_results/task_id_fixed.txt", "r") as f:
    lines = f.readlines()
    task_id = lines[0].strip()
    submitted_time = lines[1].split(": ")[1].strip() if len(lines) > 1 else "Unknown"

print(f"Monitoring Task 3: {task_id}")
print(f"Submitted: {submitted_time}")
print("-" * 50)

# Monitor until completion or timeout (60 minutes)
timeout_minutes = 60
start_time = time.time()

while True:
    try:
        task = client.get_task(task_id)
        elapsed = time.time() - start_time
        elapsed_str = f"{int(elapsed//60)}:{int(elapsed%60):02d}"

        print(f"[{elapsed_str}] Status: {task.status}")

        if task.status == "completed" or task.status == "success":
            print("\n✓ Task completed successfully!")
            break
        elif task.status in ["failed", "cancelled", "fail"]:
            print(f"\n✗ Task {task.status}")
            exit(1)

        # Check timeout
        if elapsed > timeout_minutes * 60:
            print(f"\n⏰ Timeout after {timeout_minutes} minutes")
            exit(1)

        time.sleep(30)  # Check every 30 seconds

    except Exception as e:
        print(f"Error checking task: {e}")
        time.sleep(30)

# Save results
print("\nSaving results...")
task_dict = {
    "task_id": str(task.task_id),
    "status": task.status,
    "query": task.query,
    "answer": task.answer if hasattr(task, 'answer') else None,
    "notebook": task.notebook if hasattr(task, 'notebook') else None,
    "created_at": str(task.created_at),
    "job_name": task.job_name
}

with open("output/task3_results/kosmos_raw_output_fixed.json", "w") as f:
    json.dump(task_dict, f, indent=2, default=str)

# Save notebook if it exists
if hasattr(task, 'notebook') and task.notebook:
    print("Saving notebook...")
    if hasattr(task.notebook, 'to_dict'):
        with open("output/task3_results/analysis_notebook.ipynb", "w") as f:
            json.dump(task.notebook.to_dict(), f, indent=2)
    else:
        # Try to save as string
        with open("output/task3_results/analysis_notebook.txt", "w") as f:
            f.write(str(task.notebook))

# Run evaluation
print("\nRunning evaluation...")
from task3_evaluate import evaluate_task3

metrics = evaluate_task3(
    "output/task3_results/kosmos_raw_output_fixed.json",
    "input/task3_ground_truth.json",
    "output/task3_results"
)

print("\n" + "="*50)
print("EVALUATION RESULTS")
print("="*50)
print(f"Gene Recall: {metrics.get('gene_recall', 0):.1f}% (Target: ≥66%)")
print(f"Code Execution: {metrics.get('code_execution', False)} (Target: True)")
print(f"Figure Count: {metrics.get('figure_count', 0)} (Target: ≥2)")
print(f"Hypothesis Quality: {metrics.get('hypothesis_quality', 0):.1f}% (Target: ≥50%)")
print(f"\nOverall: {'PASS' if metrics.get('overall_pass', False) else 'FAIL'}")

# Generate final report
print("\nGenerating final report...")
end_time = datetime.now()
duration = (end_time - datetime.fromisoformat(submitted_time)).total_seconds() / 60

report = f"""# Task 3: Systems Biology - Fixed Results

## Execution Summary
- **Start time:** {submitted_time}
- **End time:** {end_time.isoformat()}
- **Duration:** {duration:.1f} minutes
- **Task ID:** {task_id}
- **Status:** {task.status}

## Kosmos Query
Successfully submitted ANALYSIS job without file uploads, using inline data representation.

## Results
- **Raw output:** `kosmos_raw_output_fixed.json`
- **Notebook:** `analysis_notebook.ipynb`
- **Answer length:** {len(str(task.answer)) if hasattr(task, 'answer') and task.answer else 0} characters
- **Notebook available:** {'Yes' if hasattr(task, 'notebook') and task.notebook else 'No'}

## Metrics

| Metric | Target | Actual | Pass/Fail |
|--------|--------|--------|-----------|
| Gene recall | ≥66% | {metrics.get('gene_recall', 0):.1f}% | {'PASS' if metrics.get('gene_recall', 0) >= 66 else 'FAIL'} |
| Code execution | True | {metrics.get('code_execution', False)} | {'PASS' if metrics.get('code_execution', False) else 'FAIL'} |
| Figure count | ≥2 | {metrics.get('figure_count', 0)} | {'PASS' if metrics.get('figure_count', 0) >= 2 else 'FAIL'} |
| Hypothesis quality | ≥50% | {metrics.get('hypothesis_quality', 0):.1f}% | {'PASS' if metrics.get('hypothesis_quality', 0) >= 50 else 'FAIL'} |

## Overall Assessment
**{'PASS' if metrics.get('overall_pass', False) else 'FAIL'}**

## Files Created
- Task results: `output/task3_results/kosmos_raw_output_fixed.json`
- Analysis notebook: `output/task3_results/analysis_notebook.ipynb`
- Evaluation metrics: `output/task3_results/metrics.json`
- Task details: `output/task3_results/task_id_fixed.txt`
"""

with open("output/task3_results/task3_report_fixed.md", "w") as f:
    f.write(report)

print("\nReport saved to: output/task3_results/task3_report_fixed.md")
print("\n✓ Task 3 monitoring and evaluation completed!")