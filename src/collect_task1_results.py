#!/usr/bin/env python3
"""
Collect Task 1 results from Kosmos
"""

import json
from datetime import datetime
from pathlib import Path
from edison_wrapper import KosmosClient

# Initialize client
client = KosmosClient()

# Read task ID
with open("output/task1_results/task_id.txt", "r") as f:
    task_id = f.read().strip()

print(f"Collecting results for task: {task_id}")

# Get task details
try:
    task = client.get_task(task_id)
    print(f"Task status: {task.status}")

    if task.status == "success":
        print("Task completed successfully!")

        # Save raw output
        results_dir = Path("output/task1_results")
        output_file = results_dir / "kosmos_raw_output.json"

        # Extract result data
        if hasattr(task, 'result') and task.result:
            result_data = task.result
        elif hasattr(task, 'response'):
            result_data = task.response
        else:
            # Try to get JSON from task object
            result_data = {"task": str(task)}

        # Save to file
        with open(output_file, "w") as f:
            json.dump(result_data, f, indent=2, default=str)

        print(f"Results saved to: {output_file}")

        # Print a preview
        if isinstance(result_data, dict) and len(result_data) > 0:
            print("\nResult preview:")
            print(f"Keys: {list(result_data.keys())[:5]}")
            if 'response' in result_data or 'result' in result_data:
                content = result_data.get('response') or result_data.get('result', '')
                if isinstance(content, str):
                    print(f"Content length: {len(content)} characters")
                    print(f"First 500 chars:\n{content[:500]}...")
    else:
        print(f"Task not ready. Status: {task.status}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()