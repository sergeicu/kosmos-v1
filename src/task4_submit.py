#!/usr/bin/env python3
"""
Task 4: Submit MOLECULES job
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from edison_wrapper import KosmosClient

# Submit the job
client = KosmosClient()

query = """Design three small molecule inhibitors for the SARS-CoV-2 main protease (Mpro, also called 3CLpro) with improved oral bioavailability compared to nirmatrelvir (Paxlovid). For each molecule:
1. Provide the SMILES structure
2. Calculate ADMET properties (solubility, permeability, oral bioavailability %, CYP metabolism)
3. Predict drug-likeness (QED score, Lipinski's Rule compliance)
4. Propose a retrosynthesis route from commercially available starting materials
5. Estimate synthetic accessibility (SAScore)

Compare each designed molecule's properties to nirmatrelvir baseline."""

print(f"[{datetime.now()}] Submitting MOLECULES job...")
task_id = client.submit_molecules(query)
print(f"Task ID: {task_id}")

# Save task ID for monitoring
task_info = {
    "task_id": task_id,
    "submitted_at": datetime.now().isoformat(),
    "query": query
}

with open("../output/task4_results/task_id.json", "w") as f:
    json.dump(task_info, f, indent=2)

print(f"Task ID saved to: ../output/task4_results/task_id.json")