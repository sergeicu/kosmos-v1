#!/usr/bin/env python3
"""
Debug the failure details
"""

from edison_wrapper import KosmosClient
import json

client = KosmosClient()

# Check the failed task with files
task_id = "33fc6333-92c8-466a-a9dc-3c171fc2e22d"
print(f"Checking failed task: {task_id}")

task = client.get_task(task_id)
print(f"Status: {task.status}")
print(f"Task object type: {type(task)}")
print(f"Task attributes: {dir(task)}")

# Try to get more details
if hasattr(task, '__dict__'):
    print("\nTask __dict__:")
    for key, value in task.__dict__.items():
        print(f"  {key}: {value}")