#!/usr/bin/env python3
"""
Task 4: Structural Biology - MOLECULES Experiment
Design SARS-CoV-2 Mpro inhibitors with improved properties
"""

import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from edison_wrapper import KosmosClient

# Set up logging
log_dir = Path("../logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "task4_execution.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_molecules_task():
    """Run the MOLECULES job for designing SARS-CoV-2 Mpro inhibitors"""

    # Initialize client
    client = KosmosClient()

    # Query for SARS-CoV-2 Mpro inhibitor design
    query = """Design three small molecule inhibitors for the SARS-CoV-2 main protease (Mpro, also called 3CLpro) with improved oral bioavailability compared to nirmatrelvir (Paxlovid). For each molecule:
1. Provide the SMILES structure
2. Calculate ADMET properties (solubility, permeability, oral bioavailability %, CYP metabolism)
3. Predict drug-likeness (QED score, Lipinski's Rule compliance)
4. Propose a retrosynthesis route from commercially available starting materials
5. Estimate synthetic accessibility (SAScore)

Compare each designed molecule's properties to nirmatrelvir baseline."""

    logger.info("Submitting MOLECULES job for SARS-CoV-2 Mpro inhibitor design")
    logger.info(f"Query: {query[:100]}...")

    # Submit the job
    task_id = client.submit_molecules(query)
    logger.info(f"Task submitted with ID: {task_id}")

    # Poll for completion
    logger.info("Waiting for job completion (expected ~30 minutes)...")
    max_attempts = 360  # 30 minutes with 5-second intervals
    result = None

    for attempt in range(max_attempts):
        try:
            task = client.get_task(task_id)
            logger.info(f"Attempt {attempt + 1}/{max_attempts}: Status = {task.status}")

            if task.status == "COMPLETED":
                logger.info("Job completed successfully!")
                result = task.result
                break
            elif task.status == "FAILED":
                logger.error(f"Job failed: {task.error_message if hasattr(task, 'error_message') else 'Unknown error'}")
                return None
            elif task.status in ["CANCELLED", "TIMEOUT"]:
                logger.error(f"Job {task.status}")
                return None

            time.sleep(5)  # Wait 5 seconds between checks

        except Exception as e:
            logger.error(f"Error checking task status: {e}")
            time.sleep(5)

    if result:
        # Save raw output
        output_dir = Path("../output/task4_results")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "kosmos_raw_output.json"
        with open(output_file, 'w') as f:
            # Convert result to dict if it's not serializable
            try:
                if hasattr(result, 'dict'):
                    json.dump(result.dict(), f, indent=2)
                elif hasattr(result, '__dict__'):
                    json.dump(result.__dict__, f, indent=2)
                else:
                    json.dump(str(result), f, indent=2)
            except:
                json.dump({"result": str(result)}, f, indent=2)

        logger.info(f"Raw output saved to: {output_file}")
        return result
    else:
        logger.error("Job timed out after 30 minutes")
        return None


if __name__ == "__main__":
    logger.info("="*60)
    logger.info("TASK 4: Structural Biology - MOLECULES Experiment")
    logger.info("="*60)

    start_time = datetime.now()
    logger.info(f"Start time: {start_time}")

    try:
        result = run_molecules_task()

        if result:
            logger.info("Task 4 completed successfully!")
            logger.info("Next steps:")
            logger.info("1. Parse the results with src/task4_evaluate.py")
            logger.info("2. Generate the report")
        else:
            logger.error("Task 4 failed!")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error running Task 4: {e}")
        sys.exit(1)

    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"End time: {end_time}")
    logger.info(f"Total duration: {duration}")