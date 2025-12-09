#!/usr/bin/env python3
"""
Check Phase 1 ANALYSIS jobs to see if any succeeded
"""

from edison_wrapper import KosmosClient

client = KosmosClient()

# Check the ANALYSIS jobs from Phase 1
analysis_jobs = [
    "3df4a3a6-10e9-4c9b-b22c-6e2bbf921c67",
    "be530124-2131-4787-a28f-a58b563735e2",
    "ff0dc492-7444-471b-bac5-b2a672dbf6f2"
]

for task_id in analysis_jobs:
    print(f"\n=== Task: {task_id} ===")
    try:
        task = client.get_task(task_id)
        print(f"Status: {task.status}")
        if hasattr(task, 'answer') and task.answer:
            print(f"Has answer: Yes")
            print(f"Answer type: {type(task.answer)}")
        if hasattr(task, 'notebook') and task.notebook:
            print(f"Has notebook: Yes")
    except Exception as e:
        print(f"Error: {e}")