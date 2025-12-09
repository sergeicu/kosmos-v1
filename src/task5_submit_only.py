#!/usr/bin/env python3
"""
Task 5: Submit and monitor separately
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))
from edison_wrapper import KosmosClient

def submit_task():
    """Submit the task and save task ID"""
    client = KosmosClient()
    output_dir = Path("output/task5_results")
    output_dir.mkdir(parents=True, exist_ok=True)

    query = """What circuit-level mechanisms link gut microbiome dysbiosis to Parkinson's disease pathology, and which mechanisms are most amenable to therapeutic intervention? Rank potential interventions by current feasibility (clinical readiness, mechanistic understanding, and safety profile)."""

    print("Submitting LITERATURE task...")
    task_id = client.submit_literature(query)
    print(f"Task submitted: {task_id}")

    # Save task info
    task_info = {
        "task_id": task_id,
        "query": query,
        "submission_time": datetime.now().isoformat(),
        "job_type": "LITERATURE"
    }

    with open(output_dir / "task_id.json", "w") as f:
        json.dump(task_info, f, indent=2)

    print(f"Task ID saved to {output_dir / 'task_id.json'}")
    return task_id

def check_task(task_id):
    """Check task status and collect if complete"""
    client = KosmosClient()
    output_dir = Path("output/task5_results")

    print(f"Checking task {task_id}...")
    task = client.get_task(task_id)

    # Try to get status
    status = getattr(task, 'status', None)
    if not status and hasattr(task, 'task_status'):
        status = task.task_status

    print(f"Status: {status}")

    if status and status.lower() in ["completed", "succeeded", "success"]:
        print("Task completed! Collecting results...")

        # Try to get results
        results = getattr(task, 'results', None)
        if not results:
            results = getattr(task, 'response', None)
        if not results:
            results = getattr(task, 'output', None)
        if not results:
            results = task.__dict__ if hasattr(task, '__dict__') else str(task)

        # Save results
        raw_output = {
            "task_id": task_id,
            "collection_time": datetime.now().isoformat(),
            "results": results,
            "status": status
        }

        with open(output_dir / "kosmos_raw_output.json", "w") as f:
            json.dump(raw_output, f, indent=2, default=str)

        print(f"Results saved to {output_dir / 'kosmos_raw_output.json'}")
        return True

    return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        # Check existing task
        try:
            with open("output/task5_results/task_id.json") as f:
                task_data = json.load(f)
            task_id = task_data["task_id"]
            if check_task(task_id):
                # Run evaluation and report
                print("Running evaluation...")
                import subprocess
                subprocess.run(["python", "src/task5_evaluate.py"], check=True)
                subprocess.run(["python", "src/task5_report.py"], check=True)
        except Exception as e:
            print(f"Error checking task: {e}")
    else:
        # Submit new task
        task_id = submit_task()
        print("\nTo check status, run:")
        print(f"python {__file__} check")