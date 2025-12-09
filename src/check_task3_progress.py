#!/usr/bin/env python3
"""
Check the progress of Task 3 (fixed) execution
"""

from edison_wrapper import KosmosClient
import json
from datetime import datetime

client = KosmosClient()

# Read the task ID
try:
    with open("output/task3_results/task_id_fixed.txt", "r") as f:
        lines = f.readlines()
        task_id = lines[0].strip()
        submitted_time = lines[1].split(": ")[1].strip() if len(lines) > 1 else "Unknown"
except FileNotFoundError:
    print("Task ID file not found. Has the job been submitted?")
    exit(1)

print(f"Task ID: {task_id}")
print(f"Submitted: {submitted_time}")
print(f"Current time: {datetime.now().isoformat()}")

# Check current status
try:
    task = client.get_task(task_id)
    print(f"\nStatus: {task.status}")

    if task.status == "completed" or task.status == "success":
        print("\n✓ Task completed successfully!")

        # Check if results exist
        if os.path.exists("output/task3_results/kosmos_raw_output_fixed.json"):
            print("Results saved to: output/task3_results/kosmos_raw_output_fixed.json")
        else:
            print("Results not yet saved")

        # Check if notebook exists
        if os.path.exists("output/task3_results/successful_notebook.ipynb"):
            print("Notebook saved to: output/task3_results/successful_notebook.ipynb")

    elif task.status in ["failed", "cancelled", "fail"]:
        print(f"\n✗ Task {task.status}")
    else:
        # Still running
        elapsed = datetime.now() - datetime.fromisoformat(submitted_time)
        print(f"Elapsed time: {elapsed}")
        print("\nStill processing... (expected ~45 minutes)")

except Exception as e:
    print(f"Error checking task: {e}")

# Run evaluation if results are available
if task.status == "completed" or task.status == "success":
    import os
    if os.path.exists("output/task3_results/kosmos_raw_output_fixed.json"):
        print("\n" + "="*50)
        print("Running evaluation...")

        from task3_evaluate import evaluate_task3
        metrics = evaluate_task3(
            "output/task3_results/kosmos_raw_output_fixed.json",
            "input/task3_ground_truth.json",
            "output/task3_results"
        )

        print("\nEvaluation Results:")
        print(f"Gene Recall: {metrics.get('gene_recall', 0):.1f}%")
        print(f"Code Execution: {metrics.get('code_execution', False)}")
        print(f"Figure Count: {metrics.get('figure_count', 0)}")
        print(f"Hypothesis Quality: {metrics.get('hypothesis_quality', 0):.1f}%")
        print(f"\nOverall: {'PASS' if metrics.get('overall_pass', False) else 'FAIL'}")