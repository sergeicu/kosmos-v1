#!/usr/bin/env python3
"""
Check the failed Task 3 job and get error details
"""

from edison_wrapper import KosmosClient
import json

client = KosmosClient()

# Get the failed task
task_id = "ac0e19b3-cd73-4c45-bc28-eb63e106e2d2"
print(f"Checking task: {task_id}")

try:
    task = client.get_task(task_id)
    print(f"Task status: {task.status}")
    print(f"Task details: {task}")

    # Save task details to file
    with open("output/task3_results/failed_task_details.json", "w") as f:
        # Create a dict representation of the task
        task_dict = {
            "task_id": task_id,
            "status": task.status,
            "type": getattr(task, 'type', 'Unknown'),
            "error": getattr(task, 'error', None),
            "result": getattr(task, 'result', None)
        }
        json.dump(task_dict, f, indent=2, default=str)

    print("\nTask details saved to: output/task3_results/failed_task_details.json")

except Exception as e:
    print(f"Error getting task details: {e}")
    import traceback
    traceback.print_exc()