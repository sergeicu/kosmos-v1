#!/usr/bin/env python3
"""
Phase 2 Experiment Template

This is a complete starter template for running Kosmos experiments.
Copy this file and customize for your specific task.

Usage:
    cp phase2_experiment_template.py src/task1_run.py
    # Edit src/task1_run.py with your task-specific code
    python src/task1_run.py
"""

import os
import json
import time
import re
from datetime import datetime
from pathlib import Path

# Import working components from Phase 1
from edison_wrapper import KosmosClient


class Phase2Experiment:
    """Template for Phase 2 Kosmos experiments"""

    def __init__(self, task_name):
        self.task_name = task_name
        self.client = KosmosClient()
        self.setup_directories()

    def setup_directories(self):
        """Create required directories"""
        for dir_name in ["output", "logs"]:
            Path(dir_name).mkdir(exist_ok=True)

    def save_task_id(self, task_type, task_id):
        """Save task ID with timestamp for monitoring"""
        with open("output/submitted_tasks.txt", "a") as f:
            timestamp = datetime.now().isoformat()
            f.write(f"{timestamp} - {task_type}: {task_id}\n")
        print(f"Task ID saved: {task_id}")

    def log_execution(self, message, level="INFO"):
        """Log execution events"""
        timestamp = datetime.now().isoformat()
        log_entry = f"{timestamp} [{level}] {message}\n"

        with open(f"logs/{self.task_name}_execution.log", "a") as f:
            f.write(log_entry)

        print(message)

    def run_literature_experiment(self, query, ground_truth_file=None):
        """Run LITERATURE job (for Task 1: Cancer Genomics)"""
        self.log_execution(f"Starting LITERATURE experiment: {self.task_name}")

        try:
            # Submit job
            task_id = self.client.submit_literature(query)
            self.log_execution(f"Task submitted: {task_id}")
            self.save_task_id("LITERATURE", task_id)

            return task_id

        except Exception as e:
            self.log_execution(f"Error submitting task: {e}", "ERROR")
            return None

    def run_precedent_experiment(self, query, ground_truth_file=None):
        """Run PRECEDENT job (for Task 2: Immunology)"""
        self.log_execution(f"Starting PRECEDENT experiment: {self.task_name}")

        try:
            task_id = self.client.submit_precedent(query)
            self.log_execution(f"Task submitted: {task_id}")
            self.save_task_id("PRECEDENT", task_id)

            return task_id

        except Exception as e:
            self.log_execution(f"Error submitting task: {e}", "ERROR")
            return None

    def run_analysis_experiment(self, query, data_files, ground_truth_file=None):
        """Run ANALYSIS job (for Task 3: Systems Biology)"""
        self.log_execution(f"Starting ANALYSIS experiment: {self.task_name}")

        try:
            # Verify data files exist
            for file_path in data_files:
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"Data file not found: {file_path}")

            task_id = self.client.submit_analysis(query, files=data_files)
            self.log_execution(f"Task submitted with {len(data_files)} files: {task_id}")
            self.save_task_id("ANALYSIS", task_id)

            return task_id

        except Exception as e:
            self.log_execution(f"Error submitting task: {e}", "ERROR")
            return None

    def run_molecules_experiment(self, query, ground_truth_file=None):
        """Run MOLECULES job (for Task 4: Structural Biology)"""
        self.log_execution(f"Starting MOLECULES experiment: {self.task_name}")

        try:
            task_id = self.client.submit_molecules(query)
            self.log_execution(f"Task submitted: {task_id}")
            self.save_task_id("MOLECULES", task_id)

            return task_id

        except Exception as e:
            self.log_execution(f"Error submitting task: {e}", "ERROR")
            return None

    def monitor_task(self, task_id, timeout_minutes=60):
        """Monitor task completion"""
        self.log_execution(f"Monitoring task {task_id}")

        start_time = time.time()
        timeout_seconds = timeout_minutes * 60

        while time.time() - start_time < timeout_seconds:
            try:
                task = self.client.get_task(task_id)
                self.log_execution(f"Status: {task.status}")

                if task.status in ["completed", "success"]:
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

    def save_result(self, task, output_file="kosmos_raw_output.json"):
        """Save task result to JSON file"""
        if task and task.status in ["completed", "success"]:
            output_path = f"output/{output_file}"
            with open(output_path, "w") as f:
                if hasattr(task, 'result') and task.result:
                    json.dump(task.result, f, indent=2)
                else:
                    # If result is directly in task
                    json.dump({"result": str(task)}, f, indent=2)

            self.log_execution(f"Result saved to {output_path}")
            return True
        else:
            self.log_execution("No result to save (task not completed)", "ERROR")
            return False


def extract_nct_ids(text_or_list):
    """Extract NCT IDs from Kosmos output"""
    if isinstance(text_or_list, str):
        return re.findall(r'NCT\d{8}', text_or_list, re.IGNORECASE)
    elif isinstance(text_or_list, list):
        # If it's already a list, just return it
        return text_or_list
    return []


def verify_precedent_accuracy(kosmos_answer, ground_truth):
    """Binary: Did Kosmos correctly say Yes/No to precedent?"""
    # Extract whether Kosmos found precedent
    if isinstance(kosmos_answer, dict):
        kosmos_says = kosmos_answer.get("precedent_exists", False)
    elif isinstance(kosmos_answer, str):
        # Look for explicit yes/no in text
        if re.search(r'\b(?:yes|no)\b', kosmos_answer.lower()):
            kosmos_says = bool(re.search(r'\byes\b', kosmos_answer.lower()))
        else:
            # If NCT IDs are found, assume precedent exists
            kosmos_says = bool(extract_nct_ids(kosmos_answer))
    else:
        kosmos_says = False

    return kosmos_says == ground_truth["precedent_exists"]


def calculate_trial_recall(identified_ncts, ground_truth):
    """% of known trials found by Kosmos"""
    identified_set = set(identified_ncts)
    known_set = set([t["nct_id"] for t in ground_truth["known_trials"]])
    overlap = identified_set & known_set

    if len(known_set) == 0:
        return 0.0

    return len(overlap) / len(known_set)


def check_outcome_completeness(kosmos_output, ground_truth):
    """Does Kosmos provide outcome data for trials?"""
    # Check if outcome info is present in the output
    if isinstance(kosmos_output, str):
        has_outcomes = (
            "outcome" in kosmos_output.lower() or
            "result" in kosmos_output.lower() or
            "efficacy" in kosmos_output.lower() or
            "safety" in kosmos_output.lower() or
            "response" in kosmos_output.lower()
        )
    elif isinstance(kosmos_output, dict):
        # Check for outcome-related keys
        has_outcomes = any(
            key in kosmos_output.lower()
            for key in ["outcome", "result", "efficacy", "safety", "response"]
        )
    else:
        has_outcomes = False

    return has_outcomes


def evaluate_results(kosmos_output_file, ground_truth_file):
    """Evaluate Kosmos results against ground truth"""
    print("\n" + "="*60)
    print("EVALUATING TASK 2 RESULTS")
    print("="*60)

    # Load files
    try:
        with open(kosmos_output_file, 'r') as f:
            kosmos_output = json.load(f)

        with open(ground_truth_file, 'r') as f:
            ground_truth = json.load(f)
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    # Extract NCT IDs from Kosmos output
    kosmos_text = json.dumps(kosmos_output) if isinstance(kosmos_output, dict) else str(kosmos_output)
    identified_ncts = extract_nct_ids(kosmos_text)

    # Calculate metrics
    precedent_accuracy = verify_precedent_accuracy(kosmos_output, ground_truth)
    trial_recall = calculate_trial_recall(identified_ncts, ground_truth)
    outcome_completeness = check_outcome_completeness(kosmos_text, ground_truth)

    # Print detailed results
    print(f"\nPrecedent Question:")
    print(f"  Kosmos answer: {'Yes' if identified_ncts else 'No'}")
    print(f"  Ground truth: {'Yes' if ground_truth['precedent_exists'] else 'No'}")
    print(f"  Correct: {'✓' if precedent_accuracy else '✗'}")

    print(f"\nClinical Trials Identified:")
    for trial in ground_truth["known_trials"]:
        found = trial["nct_id"] in identified_ncts
        print(f"  {trial['nct_id']} ({trial['sponsor']}): {'✓' if found else '✗'}")

    print(f"\nRecall: {trial_recall*100:.1f}% ({len(set(identified_ncts) & set([t['nct_id'] for t in ground_truth['known_trials']]))}/{len(ground_truth['known_trials'])} trials found)")

    print(f"\nOutcome Data Quality: {'✓' if outcome_completeness else '✗'}")

    # Create metrics JSON
    metrics = {
        "trial_recall": trial_recall,
        "precedent_accuracy": precedent_accuracy,
        "outcome_completeness": outcome_completeness,
        "identified_ncts": identified_ncts,
        "timestamp": datetime.now().isoformat()
    }

    # Save metrics
    os.makedirs(os.path.dirname(kosmos_output_file), exist_ok=True)
    metrics_path = os.path.join(os.path.dirname(kosmos_output_file), "metrics.json")
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"\nMetrics saved to: {metrics_path}")

    # Generate report
    generate_report(kosmos_output_file, ground_truth_file, metrics)

    return metrics


def generate_report(kosmos_output_file, ground_truth_file, metrics):
    """Generate the Task 2 report"""
    timestamp = datetime.now().isoformat()

    # Load data for report
    with open(kosmos_output_file, 'r') as f:
        kosmos_output = json.load(f)

    with open(ground_truth_file, 'r') as f:
        ground_truth = json.load(f)

    # Create report directory
    os.makedirs(os.path.dirname(kosmos_output_file), exist_ok=True)
    report_path = os.path.join(os.path.dirname(kosmos_output_file), "task2_report.md")

    # Extract NCT IDs for report
    kosmos_text = json.dumps(kosmos_output)
    identified_ncts = extract_nct_ids(kosmos_text)

    report = f"""# Task 2: Immunology - Results

## Execution Summary
- **Start time:** {timestamp}
- **End time:** {timestamp}
- **Duration:** ~15 minutes
- **Cost:** $200

## Kosmos Query
Has anyone developed mRNA vaccines targeting solid tumor neoantigens using patient-specific mutation profiles, and what were the clinical trial outcomes?

## Ground Truth Comparison

### Precedent Question
- **Kosmos answer:** {'Yes' if identified_ncts else 'No'}
- **Ground truth:** {'Yes' if ground_truth['precedent_exists'] else 'No'}
- **Correct:** {'✓' if metrics['precedent_accuracy'] else '✗'}

### Clinical Trials Identified
| NCT ID | Found by Kosmos | In Ground Truth | Sponsor | Outcome Reported |
|--------|----------------|-----------------|---------|------------------|"""

    for trial in ground_truth["known_trials"]:
        found = trial["nct_id"] in identified_ncts
        report += f"\n| {trial['nct_id']} | {'✓' if found else '✗'} | ✓ | {trial['sponsor']} | {'✓' if found and metrics['outcome_completeness'] else '✗'} |"

    report += f"""

**Recall:** {metrics['trial_recall']*100:.1f}% ({len(set(identified_ncts) & set([t['nct_id'] for t in ground_truth['known_trials']]))}/{len(ground_truth['known_trials'])} trials found)

### Outcome Data Quality
{'Outcome data found in Kosmos output' if metrics['outcome_completeness'] else 'No outcome data found in Kosmos output'}

### Citations
| DOI | Purpose | Cited by Kosmos |
|-----|---------|-----------------|
| 10.1038/s41586-021-03368-8 | Moderna Phase 1 | {'✓' if '10.1038/s41586-021-03368-8' in kosmos_text else '✗'} |
| 10.1038/s41586-022-05400-5 | BioNTech vaccine | {'✓' if '10.1038/s41586-022-05400-5' in kosmos_text else '✗'} |

## Metrics

| Metric | Target | Actual | Pass/Fail |
|--------|--------|--------|-----------|
| Trial recall | ≥66% | {metrics['trial_recall']*100:.1f}% | {'PASS' if metrics['trial_recall'] >= 0.66 else 'FAIL'} |
| Precedent accuracy | 100% | {metrics['precedent_accuracy']*100:.1f}% | {'PASS' if metrics['precedent_accuracy'] else 'FAIL'} |
| Outcome completeness | True | {metrics['outcome_completeness']} | {'PASS' if metrics['outcome_completeness'] else 'FAIL'} |
| Key paper coverage | ≥50% | 0% | {'PASS' if False else 'FAIL'} |

## Overall Assessment
**{'PASS' if all([metrics['trial_recall'] >= 0.66, metrics['precedent_accuracy'], metrics['outcome_completeness']]) else 'FAIL'}**

## Research Gap Identification
[Research gap analysis based on Kosmos output]

## Raw Outputs
- Kosmos response: `kosmos_raw_output.json`
- Metrics: `metrics.json`
- Execution log: `../../logs/task2_execution.log`

## Notes
Kosmos identified the following NCT IDs: {', '.join(identified_ncts) if identified_ncts else 'None'}
"""

    with open(report_path, 'w') as f:
        f.write(report)

    print(f"\nReport generated: {report_path}")


# -------------------------------------------------------------------------
# CUSTOMIZE BELOW FOR YOUR SPECIFIC TASK
# -------------------------------------------------------------------------

def run_task1_cancer_genomics():
    """Task 1: Cancer Genomics - LITERATURE Job"""
    experiment = Phase2Experiment("task1_cancer_genomics")

    # Your specific query
    query = """What are the most promising targetable dependencies in KRAS-mutant
pancreatic cancer identified in the last 3 years, and what mechanisms
underlie resistance to current targeted therapies?"""

    # Run experiment
    task_id = experiment.run_literature_experiment(query)

    if task_id:
        experiment.log_execution("✓ Task 1 submitted successfully")

        # Optional: Monitor and collect result
        # task = experiment.monitor_task(task_id, timeout_minutes=20)
        # experiment.save_result(task, "task1_kosmos_output.json")
    else:
        experiment.log_execution("✗ Task 1 submission failed", "ERROR")


def run_task2_immunology():
    """Task 2: Immunology - PRECEDENT Job"""
    experiment = Phase2Experiment("task2_immunology")

    query = """Has anyone developed mRNA vaccines targeting solid tumor neoantigens
using patient-specific mutation profiles, and what were the clinical trial outcomes?"""

    # Submit the job
    task_id = experiment.run_precedent_experiment(query)

    if task_id:
        experiment.log_execution("✓ Task 2 submitted successfully")

        # Monitor the task (expected runtime ~15 minutes)
        experiment.log_execution("Starting task monitoring (expected 15 minutes)")
        task = experiment.monitor_task(task_id, timeout_minutes=25)

        # Save result if completed
        if task and task.status == "completed":
            experiment.save_result(task, "task2_results/kosmos_raw_output.json")

            # Run evaluation
            evaluate_results("output/task2_results/kosmos_raw_output.json",
                           "input/task2_ground_truth.json")

        elif task:
            experiment.log_execution(f"Task ended with status: {task.status}", "ERROR")
        else:
            experiment.log_execution("Task monitoring failed", "ERROR")
    else:
        experiment.log_execution("✗ Task 2 submission failed", "ERROR")


def run_task3_systems_biology():
    """Task 3: Systems Biology - ANALYSIS Job"""
    experiment = Phase2Experiment("task3_systems_biology")

    query = """Analyze this E. coli RNA-seq dataset from a heat shock experiment.
Identify differentially expressed genes, perform pathway enrichment analysis,
and generate 2-3 testable hypotheses about the heat shock response mechanism."""

    data_files = ["input/ecoli_heatshock.csv"]  # Your data file

    task_id = experiment.run_analysis_experiment(query, data_files)

    if task_id:
        experiment.log_execution("✓ Task 3 submitted successfully")
    else:
        experiment.log_execution("✗ Task 3 submission failed", "ERROR")


def run_task4_structural_biology():
    """Task 4: Structural Biology - MOLECULES Job"""
    experiment = Phase2Experiment("task4_structural_biology")

    query = """Design three small molecule inhibitors for the SARS-CoV-2 main protease
(Mpro) with improved oral bioavailability compared to nirmatrelvir (Paxlovid)."""

    task_id = experiment.run_molecules_experiment(query)

    if task_id:
        experiment.log_execution("✓ Task 4 submitted successfully")
    else:
        experiment.log_execution("✗ Task 4 submission failed", "ERROR")


# -------------------------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------------------------

if __name__ == "__main__":
    # Choose which task to run
    import sys

    if len(sys.argv) > 1:
        task = sys.argv[1]

        if task == "1":
            run_task1_cancer_genomics()
        elif task == "2":
            run_task2_immunology()
        elif task == "3":
            run_task3_systems_biology()
        elif task == "4":
            run_task4_structural_biology()
        else:
            print("Usage: python phase2_experiment_template.py [1|2|3|4]")
    else:
        print("Phase 2 Experiment Template")
        print("Usage: python phase2_experiment_template.py [1|2|3|4]")
        print("  1 = Task 1: Cancer Genomics")
        print("  2 = Task 2: Immunology")
        print("  3 = Task 3: Systems Biology")
        print("  4 = Task 4: Structural Biology")