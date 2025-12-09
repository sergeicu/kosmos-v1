#!/usr/bin/env python3
"""
Monitor Task 5 and automatically process when complete
"""

import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))
from edison_wrapper import KosmosClient


def monitor_and_process():
    """Monitor task until complete, then process results"""
    # Load task ID
    try:
        with open("output/task5_results/task_id.json") as f:
            task_data = json.load(f)
        task_id = task_data["task_id"]
    except Exception as e:
        print(f"Error loading task ID: {e}")
        return

    client = KosmosClient()
    output_dir = Path("output/task5_results")
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    print(f"Monitoring task {task_id}...")
    print("This may take up to 15 minutes for LITERATURE jobs.")

    # Poll for completion
    start_time = time.time()
    max_wait = 20 * 60  # 20 minutes max

    while time.time() - start_time < max_wait:
        try:
            task = client.get_task(task_id)
            status = getattr(task, 'status', None)
            if not status and hasattr(task, 'task_status'):
                status = task.task_status

            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Status: {status}")

            if status and status.lower() in ["completed", "succeeded", "success"]:
                print("\n✓ Task completed! Processing results...")

                # Get results
                results = getattr(task, 'results', None)
                if not results:
                    results = getattr(task, 'response', None)
                if not results:
                    results = getattr(task, 'output', None)
                if not results:
                    results = task.__dict__ if hasattr(task, '__dict__') else str(task)

                # Save raw results
                raw_output = {
                    "task_id": task_id,
                    "collection_time": datetime.now().isoformat(),
                    "results": results,
                    "status": status
                }

                with open(output_dir / "kosmos_raw_output.json", "w") as f:
                    json.dump(raw_output, f, indent=2, default=str)

                print(f"Results saved to {output_dir / 'kosmos_raw_output.json'}")

                # Parse results (simple extraction)
                parsed = parse_results(results)

                with open(output_dir / "parsed_results.json", "w") as f:
                    json.dump(parsed, f, indent=2)

                print("Results parsed and saved")

                # Run evaluation
                print("\nRunning evaluation...")
                import subprocess
                result = subprocess.run(["python", "src/task5_evaluate.py"],
                                      capture_output=True, text=True)
                print(result.stdout)
                if result.stderr:
                    print("Evaluation errors:", result.stderr)

                # Generate report
                print("\nGenerating report...")
                result = subprocess.run(["python", "src/task5_report.py"],
                                      capture_output=True, text=True)
                print(result.stdout)
                if result.stderr:
                    print("Report generation errors:", result.stderr)

                print(f"\n✓ All done! Results in {output_dir}/")
                return True

            elif status and status.lower() in ["failed", "error"]:
                print(f"\n✗ Task failed with status: {status}")
                # Save error info
                error_info = {
                    "task_id": task_id,
                    "status": status,
                    "timestamp": datetime.now().isoformat()
                }
                with open("logs/task5_error.log", "w") as f:
                    json.dump(error_info, f, indent=2)
                return False

            time.sleep(30)  # Check every 30 seconds

        except Exception as e:
            print(f"Error checking status: {e}")
            time.sleep(30)

    print("\n✗ Monitoring timed out after 20 minutes")
    return False


def parse_results(results):
    """Simple parsing of results to extract key information"""
    parsed = {
        "identified_mechanisms": [],
        "ranked_interventions": [],
        "citations": []
    }

    # Convert to string for text processing
    text = str(results)

    # Simple extraction using keyword matching
    sentences = text.split(". ")

    # Extract mechanisms
    for sentence in sentences:
        if any(keyword in sentence.lower()
               for keyword in ["mechanism", "pathway", "link", "connection"]):
            if len(sentence.strip()) > 20:
                parsed["identified_mechanisms"].append(sentence.strip())

    # Extract interventions
    intervention_keywords = ["intervention", "therapy", "treatment", "approach"]
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in intervention_keywords):
            if len(sentence.strip()) > 20:
                parsed["ranked_interventions"].append(sentence.strip())

    # Extract potential citations (look for DOIs or journal-like patterns)
    import re
    doi_pattern = r'10\.\d+/\w+'
    citations = re.findall(doi_pattern, text)
    parsed["citations"] = citations

    # Limit to reasonable numbers
    parsed["identified_mechanisms"] = parsed["identified_mechanisms"][:10]
    parsed["ranked_interventions"] = parsed["ranked_interventions"][:10]
    parsed["citations"] = parsed["citations"][:50]

    return parsed


if __name__ == "__main__":
    monitor_and_process()