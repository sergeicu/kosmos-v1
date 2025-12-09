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

    def save_result(self, task, output_file="kosmos_raw_output.json"):
        """Save task result to JSON file"""
        if task and task.status == "completed":
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

    task_id = experiment.run_precedent_experiment(query)

    if task_id:
        experiment.log_execution("✓ Task 2 submitted successfully")
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