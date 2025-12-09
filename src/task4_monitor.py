#!/usr/bin/env python3
"""
Monitor Task 4 job status
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from edison_wrapper import KosmosClient

# Load task ID
with open("output/task4_results/task_id.json", "r") as f:
    task_info = json.load(f)

task_id = task_info["task_id"]
print(f"Monitoring task: {task_id}")
print(f"Submitted at: {task_info['submitted_at']}")

# Initialize client
client = KosmosClient()

# Monitor status
max_checks = 360  # 30 minutes with 5-second intervals
for i in range(max_checks):
    try:
        task = client.get_task(task_id)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Check {i+1}/{max_checks}: Status = {task.status}")

        if task.status == "COMPLETED":
            print("\n✅ Task completed successfully!")

            # Save the result
            output_dir = Path("../output/task4_results")
            result_file = output_dir / "kosmos_raw_output.json"

            with open(result_file, "w") as f:
                # Try to serialize the result
                try:
                    if hasattr(task, 'result') and task.result:
                        if hasattr(task.result, 'dict'):
                            json.dump(task.result.dict(), f, indent=2)
                        elif hasattr(task.result, '__dict__'):
                            json.dump(task.result.__dict__, f, indent=2)
                        else:
                            json.dump({"result": str(task.result)}, f, indent=2)
                    else:
                        json.dump({"status": "completed", "no_result": True}, f, indent=2)
                except Exception as e:
                    json.dump({"error": str(e), "result_preview": str(task.result)[:1000]}, f, indent=2)

            print(f"Result saved to: {result_file}")
            break

        elif task.status == "FAILED":
            print(f"\n❌ Task failed!")
            if hasattr(task, 'error_message'):
                print(f"Error: {task.error_message}")
            sys.exit(1)

        elif task.status in ["CANCELLED", "TIMEOUT"]:
            print(f"\n⚠️ Task {task.status}")
            sys.exit(1)

        # If still running, wait and continue
        time.sleep(5)

    except Exception as e:
        print(f"Error checking status: {e}")
        time.sleep(5)
else:
    print("\n⏰ Task timed out after 30 minutes")
    sys.exit(1)