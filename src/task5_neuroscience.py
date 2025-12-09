#!/usr/bin/env python3
"""
Task 5: Neuroscience - LITERATURE Job
Tests Kosmos LITERATURE capability for cross-domain synthesis (microbiology + neuroscience)
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from edison_wrapper import KosmosClient


class Task5Neuroscience:
    """Run Task 5: Neuroscience LITERATURE experiment"""

    def __init__(self):
        self.client = KosmosClient()
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = self.base_dir / "output" / "task5_results"
        self.input_dir = self.base_dir / "input"
        self.logs_dir = self.base_dir / "logs"

        # Ensure directories exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.log_file = self.logs_dir / "task5_execution.log"

    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        with open(self.log_file, "a") as f:
            f.write(log_message + "\n")

    def run_kosmos_query(self):
        """Run the Kosmos LITERATURE query"""
        self.log("Starting Kosmos LITERATURE query for gut-brain-PD mechanisms")

        query = """What circuit-level mechanisms link gut microbiome dysbiosis to Parkinson's disease pathology, and which mechanisms are most amenable to therapeutic intervention? Rank potential interventions by current feasibility (clinical readiness, mechanistic understanding, and safety profile)."""

        try:
            # Submit LITERATURE job using working pattern
            task_id = self.client.submit_literature(query)
            self.log(f"LITERATURE job submitted successfully: {task_id}")

            # Save task ID
            task_info = {
                "task_id": task_id,
                "query": query,
                "submission_time": datetime.now().isoformat(),
                "job_type": "LITERATURE"
            }

            with open(self.output_dir / "task_id.json", "w") as f:
                json.dump(task_info, f, indent=2)

            return task_id

        except Exception as e:
            self.log(f"Failed to submit LITERATURE job: {str(e)}")
            raise

    def monitor_job(self, task_id):
        """Monitor job completion"""
        self.log(f"Monitoring job {task_id}...")

        # Poll for completion
        max_wait_time = 20 * 60  # 20 minutes
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            try:
                task = self.client.get_task(task_id)
                # Task object should have status attribute
                status = getattr(task, 'status', None)
                if not status and hasattr(task, 'task_status'):
                    status = task.task_status

                self.log(f"Job status: {status}")

                if status and status.lower() in ["completed", "succeeded", "success"]:
                    self.log("Job completed successfully!")
                    return True
                elif status and status.lower() in ["failed", "error"]:
                    self.log(f"Job failed with status: {status}")
                    return False

                time.sleep(30)  # Wait 30 seconds between checks

            except Exception as e:
                self.log(f"Error checking job status: {str(e)}")
                time.sleep(30)

        self.log("Job monitoring timed out")
        return False

    def collect_results(self, task_id):
        """Collect and parse results from Kosmos"""
        self.log(f"Collecting results for job {task_id}...")

        try:
            # Get task object
            task = self.client.get_task(task_id)

            # Extract results from task object
            # The task object should have results or response attribute
            results = getattr(task, 'results', None)
            if not results:
                results = getattr(task, 'response', None)
            if not results:
                results = getattr(task, 'output', None)
            if not results:
                # If all else fails, convert entire task to dict
                results = task.__dict__ if hasattr(task, '__dict__') else str(task)

            # Save raw results
            raw_output = {
                "task_id": task_id,
                "collection_time": datetime.now().isoformat(),
                "results": results
            }

            with open(self.output_dir / "kosmos_raw_output.json", "w") as f:
                json.dump(raw_output, f, indent=2, default=str)

            self.log("Results saved to kosmos_raw_output.json")

            # Parse and structure results
            parsed = self.parse_results(results)

            with open(self.output_dir / "parsed_results.json", "w") as f:
                json.dump(parsed, f, indent=2)

            self.log("Results parsed and saved")
            return parsed

        except Exception as e:
            self.log(f"Failed to collect results: {str(e)}")
            raise

    def parse_results(self, results):
        """Parse Kosmos results to extract structured information"""
        parsed = {
            "identified_mechanisms": [],
            "circuit_level_details": [],
            "ranked_interventions": [],
            "citations": [],
            "key_figures": []
        }

        # Convert results to text if it's not already
        if isinstance(results, dict):
            # If it's already structured, extract key fields
            parsed["identified_mechanisms"] = results.get("mechanisms", [])
            parsed["ranked_interventions"] = results.get("interventions", [])
            parsed["citations"] = results.get("citations", [])
        else:
            # If it's raw text, we'll need to parse it
            # For now, save as text content for manual review
            text_content = str(results)
            parsed["text_content"] = text_content

            # Simple extraction - in real implementation, use NLP
            # This is a placeholder for proper text parsing
            if "mechanism" in text_content.lower():
                # Extract sentences containing "mechanism"
                sentences = text_content.split(". ")
                for sentence in sentences:
                    if any(keyword in sentence.lower() for keyword in ["mechanism", "pathway", "circuit"]):
                        if len(sentence) > 20:  # Avoid short fragments
                            parsed["identified_mechanisms"].append(sentence.strip())

        return parsed

    def run_complete_experiment(self):
        """Run the complete Task 5 experiment"""
        self.log("=" * 60)
        self.log("Starting Task 5: Neuroscience LITERATURE Experiment")
        self.log("=" * 60)

        start_time = datetime.now()

        try:
            # Step 1: Run Kosmos query
            task_id = self.run_kosmos_query()

            # Step 2: Monitor job completion
            if not self.monitor_job(task_id):
                self.log("Job failed or timed out")
                return False

            # Step 3: Collect results
            results = self.collect_results(task_id)

            # Step 4: Run evaluation
            self.log("Running evaluation...")
            os.system(f"python {self.base_dir}/src/task5_evaluate.py")

            # Step 5: Generate report
            self.log("Generating report...")
            os.system(f"python {self.base_dir}/src/task5_report.py")

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds() / 60

            self.log("=" * 60)
            self.log(f"Task 5 completed successfully in {duration:.1f} minutes")
            self.log("=" * 60)

            return True

        except Exception as e:
            self.log(f"Task 5 failed: {str(e)}")
            # Save error information
            error_info = {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "task": "Task 5 Neuroscience"
            }

            with open(self.logs_dir / "task5_error.log", "w") as f:
                json.dump(error_info, f, indent=2)

            return False


def main():
    """Main entry point"""
    task = Task5Neuroscience()
    success = task.run_complete_experiment()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()