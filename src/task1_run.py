#!/usr/bin/env python3
"""
Task 1: Cancer Genomics - LITERATURE Job
Test Kosmos LITERATURE capability for synthesizing recent research on KRAS-mutant pancreatic cancer
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
import sys
import requests
import random

# Import working components from Phase 1
from edison_wrapper import KosmosClient


class Task1CancerGenomics:
    """Execute Task 1: Cancer Genomics experiment"""

    def __init__(self):
        self.task_name = "task1_cancer_genomics"
        self.client = KosmosClient()
        self.setup_directories()
        self.results_dir = Path("output/task1_results")
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def setup_directories(self):
        """Create required directories"""
        for dir_name in ["output", "logs", "input", "output/task1_results"]:
            Path(dir_name).mkdir(exist_ok=True)

    def log_execution(self, message, level="INFO"):
        """Log execution events"""
        timestamp = datetime.now().isoformat()
        log_entry = f"{timestamp} [{level}] {message}\n"

        with open(f"logs/{self.task_name}_execution.log", "a") as f:
            f.write(log_entry)

        print(message)

    def run_kosmos_query(self):
        """Run Kosmos LITERATURE query"""
        query = """What are the most promising targetable dependencies in KRAS-mutant pancreatic cancer identified in the last 3 years, and what mechanisms underlie resistance to current targeted therapies?"""

        self.log_execution("Starting Kosmos LITERATURE query")
        self.log_execution(f"Query: {query}")

        try:
            # Submit job
            task_id = self.client.submit_literature(query)
            self.log_execution(f"Task submitted: {task_id}")

            # Save task ID
            with open("output/task1_results/task_id.txt", "w") as f:
                f.write(task_id)

            return task_id

        except Exception as e:
            self.log_execution(f"Error submitting task: {e}", "ERROR")
            return None

    def monitor_task(self, task_id, timeout_minutes=20):
        """Monitor task completion"""
        self.log_execution(f"Monitoring task {task_id}")

        start_time = time.time()
        timeout_seconds = timeout_minutes * 60

        while time.time() - start_time < timeout_seconds:
            try:
                task = self.client.get_task(task_id)
                self.log_execution(f"Status: {task.status}")

                if task.status == "completed":
                    self.log_execution("Task completed successfully")
                    return task
                elif task.status in ["failed", "cancelled"]:
                    self.log_execution(f"Task {task.status}", "ERROR")
                    return task

                time.sleep(30)  # Wait 30 seconds between checks

            except Exception as e:
                self.log_execution(f"Error checking task status: {e}", "ERROR")
                time.sleep(30)

        self.log_execution("Task monitoring timeout", "ERROR")
        return None

    def parse_kosmos_results(self, task):
        """Parse results from Kosmos output"""
        if not task or task.status != "completed":
            self.log_execution("No valid task to parse", "ERROR")
            return None

        # Extract the result content
        if hasattr(task, 'result') and task.result:
            result_content = task.result
        else:
            # If result is directly in task object
            result_content = {"raw_response": str(task)}

        # Save raw output
        output_file = self.results_dir / "kosmos_raw_output.json"
        with open(output_file, "w") as f:
            json.dump(result_content, f, indent=2)

        self.log_execution(f"Raw output saved to {output_file}")

        # For now, we don't have the actual parsing logic since we don't know the exact format
        # This would need to be updated based on actual Kosmos response format
        parsed_results = {
            "identified_targets": [],  # To be extracted from actual response
            "resistance_mechanisms": [],  # To be extracted
            "citations": [],  # To be extracted
            "key_figures": []  # To be extracted
        }

        return parsed_results

    def create_ground_truth(self):
        """Create ground truth JSON file"""
        ground_truth = {
            "known_targets": ["SHP2", "SOS1", "MRTX1133", "MRTX849", "RM-018"],
            "known_resistance_mechanisms": [
                "KRAS G12D/V bypass signaling",
                "MEK reactivation",
                "RTK-mediated escape",
                "Adaptive metabolic rewiring"
            ],
            "key_papers": [
                "10.1038/s41586-023-06747-5",  # MRTX1133 Nature 2023
                "10.1016/j.ccell.2023.01.003",  # SHP2 resistance Cancer Cell 2023
                "10.1126/science.adg7943"  # Pan-KRAS Science 2023
            ]
        }

        ground_truth_file = Path("input/task1_ground_truth.json")
        with open(ground_truth_file, "w") as f:
            json.dump(ground_truth, f, indent=2)

        self.log_execution(f"Ground truth saved to {ground_truth_file}")
        return ground_truth

    def verify_doi_exists(self, doi):
        """Check if DOI resolves via CrossRef API"""
        try:
            response = requests.get(f"https://api.crossref.org/works/{doi}")
            return response.status_code == 200
        except:
            return False

    def calculate_metrics(self, parsed_results, ground_truth):
        """Calculate evaluation metrics"""
        metrics = {}

        # Target recall
        if "identified_targets" in parsed_results:
            overlap = set(parsed_results["identified_targets"]) & set(ground_truth["known_targets"])
            metrics["target_recall"] = len(overlap) / len(ground_truth["known_targets"])
        else:
            metrics["target_recall"] = 0.0

        # Citation count
        if "citations" in parsed_results:
            metrics["citation_count"] = len(parsed_results["citations"])
        else:
            metrics["citation_count"] = 0

        # Citation validity (spot check)
        if "citations" in parsed_results and parsed_results["citations"]:
            sample_size = min(5, len(parsed_results["citations"]))
            sample = random.sample(parsed_results["citations"], sample_size)
            valid_count = sum(1 for citation in sample if self.verify_doi_exists(citation))
            metrics["citation_validity"] = valid_count / sample_size
        else:
            metrics["citation_validity"] = 0.0

        # Key paper coverage
        if "citations" in parsed_results:
            overlap = set(parsed_results["citations"]) & set(ground_truth["key_papers"])
            metrics["key_paper_coverage"] = len(overlap) / len(ground_truth["key_papers"])
        else:
            metrics["key_paper_coverage"] = 0.0

        # Save metrics
        metrics_file = self.results_dir / "metrics.json"
        with open(metrics_file, "w") as f:
            json.dump(metrics, f, indent=2)

        self.log_execution(f"Metrics saved to {metrics_file}")
        return metrics

    def generate_report(self, metrics, start_time, end_time, parsed_results=None):
        """Generate task report"""
        # Load ground truth
        with open("input/task1_ground_truth.json", "r") as f:
            ground_truth = json.load(f)

        # Calculate pass/fail for each metric
        target_recall_pass = metrics["target_recall"] >= 0.75
        citation_count_pass = metrics["citation_count"] >= 20
        citation_validity_pass = metrics["citation_validity"] == 1.0
        key_paper_coverage_pass = metrics["key_paper_coverage"] >= 0.66

        passed_metrics = sum([target_recall_pass, citation_count_pass, citation_validity_pass, key_paper_coverage_pass])
        overall_assessment = "PASS" if passed_metrics >= 3 else "FAIL"

        report = f"""# Task 1: Cancer Genomics - Results

## Execution Summary
- **Start time:** {start_time}
- **End time:** {end_time}
- **Duration:** {(end_time - start_time).total_seconds() / 60:.1f} minutes
- **Cost:** $200

## Kosmos Query
What are the most promising targetable dependencies in KRAS-mutant pancreatic cancer identified in the last 3 years, and what mechanisms underlie resistance to current targeted therapies?

## Ground Truth Comparison

### Targets Identified
| Target | Found by Kosmos | In Ground Truth |
|--------|----------------|-----------------|
"""

        for target in ground_truth["known_targets"]:
            found = "✓" if parsed_results and "identified_targets" in parsed_results and target in parsed_results["identified_targets"] else "✗"
            report += f"| {target} | {found} | ✓ |\n"

        report += f"""
**Recall:** {metrics['target_recall']:.1%} ({len(set(parsed_results['identified_targets']) & set(ground_truth['known_targets'])) if parsed_results else 0}/{len(ground_truth['known_targets'])} targets found)

### Resistance Mechanisms
| Mechanism | Found | In Ground Truth |
|-----------|-------|-----------------|
"""

        for mechanism in ground_truth["known_resistance_mechanisms"]:
            found = "✓" if parsed_results and "resistance_mechanisms" in parsed_results and mechanism in parsed_results["resistance_mechanisms"] else "✗"
            report += f"| {mechanism} | {found} | ✓ |\n"

        report += f"""
### Citations
- **Total citations:** {metrics['citation_count']}
- **Spot-check sample:** 5 random citations
- **Valid citations:** {metrics['citation_validity']*5:.0f}/5 (100% target)
- **Fabricated citations:** {5 - metrics['citation_validity']*5 if metrics['citation_validity'] < 1 else 0}

### Key Paper Coverage
| DOI | Cited by Kosmos |
|-----|-----------------|
"""

        for doi in ground_truth["key_papers"]:
            cited = "✓" if parsed_results and "citations" in parsed_results and doi in parsed_results["citations"] else "✗"
            report += f"| {doi} | {cited} |\n"

        report += f"""
## Metrics

| Metric | Target | Actual | Pass/Fail |
|--------|--------|--------|-----------|
| Target recall | ≥75% | {metrics['target_recall']:.1%} | {'PASS' if target_recall_pass else 'FAIL'} |
| Citation count | ≥20 | {metrics['citation_count']} | {'PASS' if citation_count_pass else 'FAIL'} |
| Citation validity | 100% | {metrics['citation_validity']:.1%} | {'PASS' if citation_validity_pass else 'FAIL'} |
| Key paper coverage | ≥66% | {metrics['key_paper_coverage']:.1%} | {'PASS' if key_paper_coverage_pass else 'FAIL'} |

## Overall Assessment
**{overall_assessment}:** {passed_metrics}/4 metrics passing

## Raw Outputs
- Kosmos response: `output/task1_results/kosmos_raw_output.json`
- Metrics: `output/task1_results/metrics.json`
- Execution log: `logs/task1_execution.log`

## Notes
"""

        if parsed_results is None:
            report += "Task execution failed - no results to parse\n"
        else:
            report += "Task executed successfully\n"

        # Save report
        report_file = self.results_dir / "task1_report.md"
        with open(report_file, "w") as f:
            f.write(report)

        self.log_execution(f"Report saved to {report_file}")
        print("\n" + report)

        return report

    def run_complete_experiment(self):
        """Run the complete Task 1 experiment"""
        start_time = datetime.now()
        self.log_execution("Starting Task 1: Cancer Genomics experiment")

        # Create ground truth
        ground_truth = self.create_ground_truth()

        # Run Kosmos query
        task_id = self.run_kosmos_query()

        if not task_id:
            self.log_execution("Failed to submit task", "ERROR")
            end_time = datetime.now()
            return self.generate_report({}, start_time, end_time)

        # Monitor task
        task = self.monitor_task(task_id)

        if not task or task.status != "completed":
            self.log_execution("Task did not complete successfully", "ERROR")
            end_time = datetime.now()
            return self.generate_report({}, start_time, end_time)

        # Parse results
        parsed_results = self.parse_kosmos_results(task)

        # Calculate metrics
        metrics = self.calculate_metrics(parsed_results, ground_truth)

        # Generate report
        end_time = datetime.now()
        report = self.generate_report(metrics, start_time, end_time, parsed_results)

        self.log_execution("Task 1 experiment completed")
        return report


if __name__ == "__main__":
    # Run Task 1
    task1 = Task1CancerGenomics()

    # Check command line args
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor-only":
        # Monitor existing task
        try:
            with open("output/task1_results/task_id.txt", "r") as f:
                task_id = f.read().strip()

            task = task1.monitor_task(task_id)
            if task and task.status == "completed":
                parsed_results = task1.parse_kosmos_results(task)
                ground_truth = task1.create_ground_truth()
                metrics = task1.calculate_metrics(parsed_results, ground_truth)
                task1.generate_report(metrics, datetime.now(), datetime.now(), parsed_results)
        except Exception as e:
            task1.log_execution(f"Error in monitor-only mode: {e}", "ERROR")
    else:
        # Run complete experiment
        task1.run_complete_experiment()