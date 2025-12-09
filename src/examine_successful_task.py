#!/usr/bin/env python3
"""
Examine the successful ANALYSIS task (without files)
"""

from edison_wrapper import KosmosClient
import json

client = KosmosClient()

task_id = "5a3d9af8-91ef-4825-8462-aece611860f4"
print(f"Examining successful task: {task_id}")

task = client.get_task(task_id)
print(f"Status: {task.status}")

# Save the full task response
with open("output/task3_results/successful_task_no_files.json", "w") as f:
    task_dict = {
        "task_id": str(task.task_id),
        "status": task.status,
        "query": task.query,
        "answer": task.answer if hasattr(task, 'answer') else None,
        "notebook": task.notebook if hasattr(task, 'notebook') else None,
        "created_at": str(task.created_at),
        "job_name": task.job_name
    }
    json.dump(task_dict, f, indent=2, default=str)

print("\nTask saved to: output/task3_results/successful_task_no_files.json")

if hasattr(task, 'answer') and task.answer:
    print(f"\nAnswer length: {len(str(task.answer))}")
    print(f"Answer preview: {str(task.answer)[:200]}...")

if hasattr(task, 'notebook') and task.notebook:
    print(f"\nNotebook available: Yes")
    # Save notebook separately if it exists
    if hasattr(task.notebook, 'to_dict'):
        with open("output/task3_results/successful_notebook.ipynb", "w") as f:
            json.dump(task.notebook.to_dict(), f, indent=2)
        print("Notebook saved to: output/task3_results/successful_notebook.ipynb")