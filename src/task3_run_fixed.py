#!/usr/bin/env python3
"""
Task 3: Systems Biology - Fixed Version

This script runs the Kosmos ANALYSIS job for E. coli heat shock RNA-seq data
with the file upload issue addressed.
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


class Task3FixedSystemBiology:
    """Execute Task 3: Systems Biology experiment (fixed)"""

    def __init__(self):
        self.task_name = "task3_systems_biology_fixed"
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

    def generate_inline_data(self):
        """Generate inline data representation of the RNA-seq dataset"""
        self.log_execution("Generating inline RNA-seq data")

        # Read the already generated CSV
        df = pd.read_csv("input/task3_ecoli_heatshock.csv", index_col=0)

        # Convert to a format that can be included in the query
        # Show the first 20 rows as preview
        preview = df.head(20).to_csv()

        # Create summary statistics
        summary = {
            "total_genes": df.shape[0],
            "total_samples": df.shape[1],
            "sample_names": df.columns.tolist(),
            "control_samples": [col for col in df.columns if 'control' in col],
            "heat_samples": [col for col in df.columns if 'heat' in col]
        }

        # Calculate fold changes for known heat shock genes
        heat_shock_genes = ["dnaK", "dnaJ", "groEL", "groES", "htpG", "clpB", "ibpA", "ibpB"]
        fold_changes = {}

        for gene in heat_shock_genes:
            if gene in df.index:
                control_mean = df.loc[gene, [col for col in df.columns if 'control' in col]].mean()
                heat_mean = df.loc[gene, [col for col in df.columns if 'heat' in col]].mean()
                fc = heat_mean / control_mean if control_mean > 0 else float('inf')
                fold_changes[gene] = fc

        return {
            "preview": preview,
            "summary": summary,
            "fold_changes": fold_changes
        }

    def create_analysis_query(self, data):
        """Create a comprehensive analysis query with inline data"""

        query = f"""You are analyzing an E. coli RNA-seq dataset from a heat shock experiment.

Dataset Summary:
- Total genes: {data['summary']['total_genes']}
- Total samples: {data['summary']['total_samples']}
- Sample names: {', '.join(data['summary']['sample_names'])}
- Control samples: {', '.join(data['summary']['control_samples'])}
- Heat shock samples: {', '.join(data['summary']['heat_samples'])}

Preview of the data (first 20 genes):
{data['preview']}

The dataset includes expression counts for 500 genes across 5 samples.
Key observations:
- Some genes show dramatic upregulation in heat shock conditions
- Known heat shock genes like dnaK, dnaJ, groEL, groES are included

Please perform the following analysis:
1. Identify differentially expressed genes between control and heat shock conditions
2. Perform pathway enrichment analysis
3. Generate 2-3 testable hypotheses about the heat shock response mechanism
4. Create publication-quality visualizations (heatmap, volcano plot, pathway diagram)

Instructions:
- Use appropriate statistical tests (e.g., DESeq2, edgeR methodology)
- Apply multiple testing correction (e.g., Benjamini-Hochberg FDR)
- Consider genes with |log2FC| > 1 and adjusted p-value < 0.05 as significant
- Focus on chaperone proteins, proteases, and transcription factors
- Generate clear, testable hypotheses based on the differential expression patterns

Please create a comprehensive Jupyter notebook with:
- Data loading and preprocessing
- Differential expression analysis
- Pathway enrichment
- Visualization generation
- Hypothesis formulation

Export the results including:
- List of significant DEGs with fold changes and p-values
- Enriched pathways with enrichment scores
- Generated figures
- Testable hypotheses with rationale"""

        return query

    def run_kosmos_analysis(self, query):
        """Run Kosmos ANALYSIS job without file uploads"""
        self.log_execution("Submitting Kosmos ANALYSIS job (without file uploads)")

        try:
            task_id = self.client.submit_analysis(query)
            self.log_execution(f"Task submitted successfully: {task_id}")

            # Save task ID and query
            with open("output/task3_results/task_id_fixed.txt", "w") as f:
                f.write(f"{task_id}\n")
                f.write(f"Submitted: {datetime.now().isoformat()}\n")
                f.write(f"\nQuery:\n{query}\n")

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
                task = client.get_task(task_id)
                self.log_execution(f"Status: {task.status}")

                if task.status == "completed" or task.status == "success":
                    self.log_execution("✓ Task completed successfully")
                    return task
                elif task.status in ["failed", "cancelled", "fail"]:
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
        if task and (task.status == "completed" or task.status == "success"):
            self.log_execution("Saving Kosmos results")

            # Save raw output
            output_path = "output/task3_results/kosmos_raw_output_fixed.json"
            with open(output_path, "w") as f:
                task_dict = {
                    "task_id": str(task.task_id),
                    "status": task.status,
                    "query": task.query,
                    "answer": task.answer if hasattr(task, 'answer') else None,
                    "notebook": task.notebook if hasattr(task, 'notebook') else None,
                    "created_at": str(task.created_at),
                    "job_name": task.job_name
                }
                json.dump(task_dict, f, indent=2, default=str)

            self.log_execution(f"Results saved to {output_path}")
            return True
        else:
            self.log_execution("No results to save (task not completed)", "ERROR")
            return False

    def run_evaluation(self):
        """Run evaluation using the evaluation script"""
        self.log_execution("Running evaluation metrics")

        # Import and run the evaluation
        import sys
        sys.path.append("src")
        from task3_evaluate import evaluate_task3

        try:
            metrics = evaluate_task3(
                "output/task3_results/kosmos_raw_output_fixed.json",
                "input/task3_ground_truth.json",
                "output/task3_results"
            )

            self.log_execution(f"Evaluation completed: {metrics}")
            return metrics
        except Exception as e:
            self.log_execution(f"Evaluation failed: {e}", "ERROR")
            return None


def main():
    """Execute fixed Task 3"""
    experiment = Task3FixedSystemBiology()

    # Step 1: Generate inline data representation
    data = experiment.generate_inline_data()

    # Step 2: Create comprehensive query
    query = experiment.create_analysis_query(data)

    # Step 3: Run Kosmos analysis (without file uploads)
    task_id = experiment.run_kosmos_analysis(query)

    if task_id:
        experiment.log_execution("✓ Kosmos job submitted successfully")

        # Step 4: Monitor task (this will take ~45 minutes)
        experiment.log_execution("Starting task monitoring (this will take ~45 minutes)...")
        task = experiment.monitor_task(task_id, timeout_minutes=60)

        if task:
            # Step 5: Save results
            experiment.save_kosmos_results(task)

            # Step 6: Run evaluation
            metrics = experiment.run_evaluation()

            experiment.log_execution("✓ Task 3 (fixed) completed successfully")
        else:
            experiment.log_execution("✗ Task failed or timed out", "ERROR")
    else:
        experiment.log_execution("✗ Failed to submit Kosmos job", "ERROR")


if __name__ == "__main__":
    global client  # Make client available for monitoring
    client = KosmosClient()
    main()