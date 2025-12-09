#!/usr/bin/env python3
"""
Collect results from already completed Task 2
"""

import os
import json
from datetime import datetime
from edison_wrapper import KosmosClient

# Task ID from the previous run
TASK_ID = "9e573c63-aa7d-4f79-adc3-501ffc4ba279"

def collect_result():
    """Collect and evaluate the completed task result"""
    client = KosmosClient()

    print(f"Collecting result for task: {TASK_ID}")

    # Get the task
    task = client.get_task(TASK_ID)
    print(f"Task status: {task.status}")

    if task.status in ["completed", "success"]:
        print("Task completed successfully!")

        # Save raw output
        output_path = "output/task2_results/kosmos_raw_output.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            if hasattr(task, 'result') and task.result:
                json.dump(task.result, f, indent=2)
            else:
                # If result is directly in task object, try to serialize
                result = {
                    "status": task.status,
                    "result": str(task) if not hasattr(task, 'result') else task.result
                }
                json.dump(result, f, indent=2)

        print(f"Result saved to: {output_path}")

        # Run evaluation
        exec(open('src/task2_run.py').read().split('# -----------------------------------------------------------------')[1].split('def evaluate_results')[0])
        evaluate_results(output_path, "input/task2_ground_truth.json")

    else:
        print(f"Task not completed. Status: {task.status}")

if __name__ == "__main__":
    collect_result()