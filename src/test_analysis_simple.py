#!/usr/bin/env python3
"""
Simple test of ANALYSIS job to debug the issue
"""

from edison_wrapper import KosmosClient
import os
import pandas as pd

# Create a very simple CSV for testing
simple_data = {
    "gene": ["gene1", "gene2", "gene3"],
    "control": [10, 20, 30],
    "treatment": [100, 200, 300]
}
df = pd.DataFrame(simple_data)
df.to_csv("input/simple_test.csv", index=False)

print(f"Created simple test CSV: {df.shape}")
print(df)

# Test with the simple data
client = KosmosClient()

# Test 1: Submit without any files
print("\n=== Test 1: ANALYSIS without files ===")
try:
    task_id = client.submit_analysis("Just say hello and confirm you received this query")
    print(f"Task submitted without files: {task_id}")
except Exception as e:
    print(f"Error submitting without files: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Submit with the simple CSV
print("\n=== Test 2: ANALYSIS with simple CSV ===")
try:
    # Use absolute path
    csv_path = os.path.abspath("input/simple_test.csv")
    print(f"Using CSV path: {csv_path}")
    print(f"File exists: {os.path.exists(csv_path)}")

    task_id = client.submit_analysis(
        "Analyze this simple dataset. What are the gene names?",
        files=[csv_path]
    )
    print(f"Task submitted with simple CSV: {task_id}")
except Exception as e:
    print(f"Error submitting with files: {e}")
    import traceback
    traceback.print_exc()