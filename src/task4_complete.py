#!/usr/bin/env python3
"""
Task 4: Complete workflow - monitor, evaluate, and report
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from edison_wrapper import KosmosClient

def run_complete_workflow():
    """Run the complete Task 4 workflow"""

    print("="*60)
    print("TASK 4: STRUCTURAL BIOLOGY - COMPLETE WORKFLOW")
    print("="*60)

    # Load task ID
    try:
        with open("output/task4_results/task_id.json", "r") as f:
            task_info = json.load(f)
        task_id = task_info["task_id"]
        print(f"\nTask ID: {task_id}")
        print(f"Submitted: {task_info['submitted_at']}")
    except:
        print("\n❌ Error: Task ID file not found. Please run task4_submit.py first.")
        sys.exit(1)

    # Initialize client
    client = KosmosClient()

    # Monitor and wait for completion
    print("\nMonitoring job progress...")
    max_checks = 360  # 30 minutes with 5-second intervals
    completed = False

    for i in range(max_checks):
        try:
            task = client.get_task(task_id)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Status: {task.status}")

            if task.status == "COMPLETED":
                print("\n✅ Job completed successfully!")
                completed = True
                break

            elif task.status == "FAILED":
                print(f"\n❌ Job failed!")
                if hasattr(task, 'error_message'):
                    print(f"Error: {task.error_message}")

                # Save error
                error_info = {
                    "task_id": task_id,
                    "status": "FAILED",
                    "error": getattr(task, 'error_message', 'Unknown error'),
                    "timestamp": datetime.now().isoformat()
                }

                with open("output/task4_results/error.json", "w") as f:
                    json.dump(error_info, f, indent=2)

                sys.exit(1)

            elif task.status in ["CANCELLED", "TIMEOUT"]:
                print(f"\n⚠️ Job {task.status}")
                sys.exit(1)

            time.sleep(5)

        except Exception as e:
            print(f"Error checking status: {e}")
            time.sleep(5)

    if not completed:
        print("\n⏰ Job timed out after 30 minutes")
        sys.exit(1)

    # Save the results
    print("\nSaving results...")
    output_dir = Path("output/task4_results")
    result_file = output_dir / "kosmos_raw_output.json"

    with open(result_file, "w") as f:
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

    print(f"✅ Results saved to: {result_file}")

    # Run evaluation
    print("\n" + "="*60)
    print("RUNNING EVALUATION")
    print("="*60)

    try:
        # Import and run evaluation
        import importlib.util
        spec = importlib.util.spec_from_file_location("task4_evaluate", "task4_evaluate.py")
        eval_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(eval_module)

        metrics, molecules = eval_module.main()
        print("\n✅ Evaluation completed")
    except Exception as e:
        print(f"\n❌ Evaluation failed: {e}")
        sys.exit(1)

    # Generate report
    print("\n" + "="*60)
    print("GENERATING REPORT")
    print("="*60)

    try:
        # Import and run report generation
        spec = importlib.util.spec_from_file_location("task4_generate_report", "task4_generate_report.py")
        report_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(report_module)

        print("\n✅ Report generated")
    except Exception as e:
        print(f"\n❌ Report generation failed: {e}")
        sys.exit(1)

    # Final summary
    print("\n" + "="*60)
    print("TASK 4 COMPLETED")
    print("="*60)
    print(f"\nAll outputs saved to: {output_dir}")
    print("- task_id.json: Job submission info")
    print("- kosmos_raw_output.json: Raw API response")
    print("- parsed_molecules.json: Extracted molecular data")
    print("- metrics.json: Evaluation metrics")
    print("- task4_report.md: Final report")

    # Determine overall success
    success = all([
        metrics['chemical_validity_pct'] >= 100,
        metrics['admet_completeness_pct'] >= 100,
        metrics['property_improvement_pct'] >= 66,
        metrics['synthesis_provided_pct'] >= 100
    ])

    print(f"\nOverall Result: {'✅ PASS' if success else '❌ FAIL'}")

    if success:
        print("\n🎉 Task 4 completed successfully!")
        print("All targets met for the structural biology experiment.")
    else:
        print("\n⚠️ Task 4 completed but targets not fully met.")
        print("See task4_report.md for detailed analysis.")

    return success


if __name__ == "__main__":
    start_time = datetime.now()
    print(f"Start time: {start_time}")

    try:
        success = run_complete_workflow()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Task interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)