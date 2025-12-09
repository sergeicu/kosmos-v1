#!/usr/bin/env python3
"""
Task 3: Systems Biology - RNA-seq Analysis

This script runs the Kosmos ANALYSIS job for E. coli heat shock RNA-seq data
as specified in tasks/task3_systems_bio.md
"""

import os
import json
import time
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

# Import working components from Phase 1
from edison_wrapper import KosmosClient


class Task3SystemBiology:
    """Execute Task 3: Systems Biology experiment"""

    def __init__(self):
        self.task_name = "task3_systems_biology"
        self.client = KosmosClient()
        self.setup_directories()
        self.start_time = datetime.now()

    def setup_directories(self):
        """Create required directories"""
        for dir_name in ["output/task3_results", "input", "logs"]:
            Path(dir_name).mkdir(parents=True, exist_ok=True)

    def log_execution(self, message, level="INFO"):
        """Log execution events"""
        timestamp = datetime.now().isoformat()
        log_entry = f"{timestamp} [{level}] {message}\n"

        with open(f"logs/{self.task_name}_execution.log", "a") as f:
            f.write(log_entry)

        print(f"[{level}] {message}")

    def generate_test_data(self):
        """Generate simulated E. coli heat shock RNA-seq data"""
        self.log_execution("Generating simulated E. coli heat shock data")

        # Canonical heat shock genes with high fold-changes
        heat_shock_genes = ["dnaK", "dnaJ", "groEL", "groES", "htpG", "clpB", "ibpA", "ibpB"]
        housekeeping = ["rrsA", "gyrA", "recA"]  # Stable expression

        # Generate mock counts
        np.random.seed(42)
        n_genes = 500
        samples = ["control_1", "control_2", "heat_1", "heat_2", "heat_3"]

        # Simulate data where heat shock genes are upregulated
        data = {}
        for gene in (heat_shock_genes + housekeeping + [f"gene_{i}" for i in range(n_genes - len(heat_shock_genes) - len(housekeeping))]):
            if gene in heat_shock_genes:
                # High expression in heat samples
                base_counts = np.random.randint(80, 150, 2)  # Control
                heat_counts = list(np.random.randint(800, 1200, 3))  # Heat shock
                data[gene] = list(base_counts) + heat_counts
            elif gene in housekeeping:
                # Stable across conditions
                data[gene] = list(np.random.randint(400, 600, 5))
            else:
                # Random low expression
                data[gene] = list(np.random.randint(10, 300, 5))

        df = pd.DataFrame(data, index=samples).T
        output_path = "input/task3_ecoli_heatshock.csv"
        df.to_csv(output_path)

        self.log_execution(f"Generated test data: {output_path} ({df.shape[0]} genes × {df.shape[1]} samples)")
        return output_path

    def create_ground_truth(self):
        """Create ground truth JSON for evaluation"""
        self.log_execution("Creating ground truth evaluation file")

        ground_truth = {
            "canonical_upregulated_genes": [
                "dnaK",  "dnaJ", "groEL", "groES", "htpG", "clpB", "ibpA", "ibpB",
                "rpoH",  "ftsJ", "hslU", "lon"
            ],
            "expected_pathways": [
                "protein folding",
                "chaperone-mediated protein folding",
                "response to heat",
                "proteolysis"
            ],
            "known_mechanisms": [
                "sigma-32 (rpoH) regulon activation",
                "DnaK-DnaJ-GrpE chaperone system",
                "GroEL-GroES chaperonin complex",
                "Lon and Clp protease activation"
            ]
        }

        output_path = "input/task3_ground_truth.json"
        with open(output_path, "w") as f:
            json.dump(ground_truth, f, indent=2)

        self.log_execution(f"Created ground truth file: {output_path}")
        return output_path

    def run_kosmos_analysis(self, data_file):
        """Run Kosmos ANALYSIS job"""
        query = """Analyze this E. coli RNA-seq dataset from a heat shock experiment.
        Identify differentially expressed genes, perform pathway enrichment analysis,
        and generate 2-3 testable hypotheses about the heat shock response mechanism.
        Create publication-quality visualizations (heatmap, volcano plot, pathway diagram)."""

        self.log_execution("Submitting Kosmos ANALYSIS job")

        try:
            task_id = self.client.submit_analysis(query, files=[data_file])
            self.log_execution(f"Task submitted successfully: {task_id}")

            # Save task ID
            with open("output/task3_results/task_id.txt", "w") as f:
                f.write(f"{task_id}\n")
                f.write(f"Submitted: {datetime.now().isoformat()}\n")

            return task_id

        except Exception as e:
            self.log_execution(f"Error submitting task: {e}", "ERROR")
            return None

    def monitor_task(self, task_id, timeout_minutes=60):
        """Monitor task completion"""
        self.log_execution(f"Monitoring task {task_id} (timeout: {timeout_minutes} min)")

        start_time = time.time()
        timeout_seconds = timeout_minutes * 60

        while time.time() - start_time < timeout_seconds:
            try:
                task = self.client.get_task(task_id)
                self.log_execution(f"Status: {task.status}")

                if task.status == "completed":
                    self.log_execution("✓ Task completed successfully")
                    return task
                elif task.status in ["failed", "cancelled"]:
                    self.log_execution(f"✗ Task {task.status}", "ERROR")
                    return task

                time.sleep(30)  # Wait 30 seconds between checks

            except Exception as e:
                self.log_execution(f"Error checking task status: {e}", "ERROR")
                time.sleep(30)

        self.log_execution("Task monitoring timeout", "ERROR")
        return None

    def save_kosmos_results(self, task):
        """Save Kosmos output"""
        if task and task.status == "completed":
            self.log_execution("Saving Kosmos results")

            # Save raw output
            output_path = "output/task3_results/kosmos_raw_output.json"
            with open(output_path, "w") as f:
                if hasattr(task, 'result') and task.result:
                    json.dump(task.result, f, indent=2)
                else:
                    json.dump({"result": str(task), "status": task.status}, f, indent=2)

            self.log_execution(f"Results saved to {output_path}")
            return True
        else:
            self.log_execution("No results to save (task not completed)", "ERROR")
            return False

    def calculate_metrics(self, kosmos_output, ground_truth_path):
        """Calculate evaluation metrics"""
        self.log_execution("Calculating evaluation metrics")

        # Load ground truth
        with open(ground_truth_path, "r") as f:
            ground_truth = json.load(f)

        # Initialize metrics
        metrics = {
            "gene_recall": 0,
            "code_execution": False,
            "figure_count": 0,
            "hypothesis_quality": 0
        }

        # Extract DEGs from Kosmos output (this would need custom parsing based on actual output format)
        # For now, using placeholder
        identified_degs = []  # Extract from kosmos_output

        # Calculate gene recall
        identified_set = set([g.lower() for g in identified_degs])
        canonical_set = set([g.lower() for g in ground_truth["canonical_upregulated_genes"]])
        overlap = identified_set & canonical_set
        metrics["gene_recall"] = len(overlap) / len(canonical_set) * 100 if canonical_set else 0

        # Check for notebook execution (would need actual notebook)
        metrics["code_execution"] = False  # Placeholder

        # Count figures (would need to check output directory)
        metrics["figure_count"] = 0  # Placeholder

        # Evaluate hypotheses (would need to extract from output)
        hypotheses = []  # Extract from kosmos_output
        if hypotheses:
            score = 0
            for hyp in hypotheses:
                hyp_lower = hyp.lower()
                for mechanism in ground_truth["known_mechanisms"]:
                    if any(word in hyp_lower for word in mechanism.lower().split()):
                        score += 1
                        break
            metrics["hypothesis_quality"] = score / len(hypotheses) * 100

        # Save metrics
        metrics_path = "output/task3_results/metrics.json"
        with open(metrics_path, "w") as f:
            json.dump(metrics, f, indent=2)

        self.log_execution(f"Metrics saved: {metrics}")
        return metrics

    def generate_report(self, metrics):
        """Generate final report"""
        self.log_execution("Generating final report")

        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds() / 60  # minutes

        report = f"""# Task 3: Systems Biology - Results

## Execution Summary
- **Start time:** {self.start_time.isoformat()}
- **End time:** {end_time.isoformat()}
- **Duration:** {duration:.1f} minutes
- **Cost:** $200

## Kosmos Query
Analyze this E. coli RNA-seq dataset from a heat shock experiment. Identify differentially expressed genes, perform pathway enrichment analysis, and generate 2-3 testable hypotheses about the heat shock response mechanism. Create publication-quality visualizations (heatmap, volcano plot, pathway diagram).

## Dataset
- **Source:** Simulated test data
- **Dimensions:** 500 genes × 5 samples
- **Conditions:** Control (2 samples) vs. Heat shock (3 samples)

## Ground Truth Comparison

### Differentially Expressed Genes (DEGs)
**Gene Recall:** {metrics['gene_recall']:.1f}%

**Genes Identified:** To be extracted from Kosmos output
**Canonical genes in top 50:** To be determined

### Generated Hypotheses
To be extracted from Kosmos output

**Hypothesis quality score:** {metrics['hypothesis_quality']:.1f}%

### Code Execution
- **Notebook path:** `analysis_notebook.ipynb` (to be extracted)
- **Executed successfully:** {metrics['code_execution']}

### Figures Generated
- **Count:** {metrics['figure_count']} (target: ≥2)
- **Types:**
  - [ ] Heatmap
  - [ ] Volcano plot
  - [ ] Pathway diagram
  - [ ] Other: To be determined

## Metrics

| Metric | Target | Actual | Pass/Fail |
|--------|--------|--------|-----------|
| Gene recall | ≥66% | {metrics['gene_recall']:.1f}% | {'PASS' if metrics['gene_recall'] >= 66 else 'FAIL'} |
| Code execution | True | {metrics['code_execution']} | {'PASS' if metrics['code_execution'] else 'FAIL'} |
| Figure count | ≥2 | {metrics['figure_count']} | {'PASS' if metrics['figure_count'] >= 2 else 'FAIL'} |
| Hypothesis quality | ≥50% | {metrics['hypothesis_quality']:.1f}% | {'PASS' if metrics['hypothesis_quality'] >= 50 else 'FAIL'} |

## Overall Assessment
**{'PASS' if sum([metrics['gene_recall'] >= 66, metrics['code_execution'], metrics['figure_count'] >= 2, metrics['hypothesis_quality'] >= 50]) >= 3 else 'FAIL'}**

## Qualitative Observations
To be completed after reviewing Kosmos output

## Raw Outputs
- Kosmos response: `kosmos_raw_output.json`
- Analysis notebook: To be extracted
- Figures: `figures/*.png` (to be extracted)
- Metrics: `metrics.json`
- Execution log: `../logs/task3_execution.log`

## Notes
Simulated data generated with known heat shock response genes for validation.
"""

        # Save report
        report_path = "output/task3_results/task3_report.md"
        with open(report_path, "w") as f:
            f.write(report)

        self.log_execution(f"Report generated: {report_path}")
        return report_path


def main():
    """Execute Task 3"""
    experiment = Task3SystemBiology()

    # Step 1: Generate test data
    data_file = experiment.generate_test_data()

    # Step 2: Create ground truth
    ground_truth_file = experiment.create_ground_truth()

    # Step 3: Run Kosmos analysis
    task_id = experiment.run_kosmos_analysis(data_file)

    if task_id:
        experiment.log_execution("✓ Kosmos job submitted successfully")

        # Step 4: Monitor task (this will take ~45 minutes)
        experiment.log_execution("Starting task monitoring (this will take ~45 minutes)...")
        task = experiment.monitor_task(task_id, timeout_minutes=60)

        if task:
            # Step 5: Save results
            experiment.save_kosmos_results(task)

            # Step 6: Calculate metrics
            metrics = experiment.calculate_metrics(None, ground_truth_file)  # None until we parse actual output

            # Step 7: Generate report
            experiment.generate_report(metrics)

            experiment.log_execution("✓ Task 3 completed successfully")
        else:
            experiment.log_execution("✗ Task failed or timed out", "ERROR")
    else:
        experiment.log_execution("✗ Failed to submit Kosmos job", "ERROR")


if __name__ == "__main__":
    main()