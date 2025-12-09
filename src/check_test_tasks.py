#!/usr/bin/env python3
"""
Check the status of our test tasks
"""

from edison_wrapper import KosmosClient
import time

client = KosmosClient()

# Check both test tasks
tasks = [
    ("5a3d9af8-91ef-4825-8462-aece611860f4", "No files"),
    ("33fc6333-92c8-466a-a9dc-3c171fc2e22d", "With CSV")
]

for task_id, description in tasks:
    print(f"\n=== Task: {task_id} ({description}) ===")
    try:
        task = client.get_task(task_id)
        print(f"Status: {task.status}")
        if hasattr(task, 'error') and task.error:
            print(f"Error: {task.error}")
        if hasattr(task, 'result') and task.result:
            print(f"Result: {task.result}")
    except Exception as e:
        print(f"Error checking task: {e}")