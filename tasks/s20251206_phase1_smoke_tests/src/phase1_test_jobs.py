import pytest
import os
from dotenv import load_dotenv

load_dotenv()

def test_literature_job_submits():
    """Can we submit a LITERATURE job?"""
    from edison_client import EdisonClient, JobNames, TaskRequest

    client = EdisonClient(api_key=os.getenv("EDISON_API_KEY"))

    try:
        # Minimal LITERATURE query
        task_request = TaskRequest(
            name=JobNames.LITERATURE,
            query="What is CRISPR-Cas9?"
        )

        response = client.create_task(task_request)

        # Verify task was accepted
        assert response is not None, "Task submission returned None"

        # Response is the task_id directly (as string UUID)
        task_id = str(response)
        assert task_id is not None, "task_id is None"
        assert len(task_id) > 0, "task_id is empty"

        print(f"✓ LITERATURE task submitted: {task_id}")

        # Save task_id for monitoring
        with open("output/phase1_results/submitted_jobs.txt", "a") as f:
            f.write(f"LITERATURE: {task_id}\n")

    except Exception as e:
        pytest.fail(f"LITERATURE task submission failed: {e}")


def test_analysis_job_submits():
    """Can we submit an ANALYSIS job?"""
    from edison_client import EdisonClient, JobNames, TaskRequest

    client = EdisonClient(api_key=os.getenv("EDISON_API_KEY"))

    # Create minimal test data
    test_data_path = "input/test_data.csv"
    with open(test_data_path, 'w') as f:
        f.write("gene,sample1,sample2\n")
        f.write("GAPDH,100,120\n")
        f.write("ACTB,150,140\n")

    try:
        # Try creating ANALYSIS task with file
        task_request = TaskRequest(
            name=JobNames.ANALYSIS,
            query="Describe this dataset"
        )

        # Attempt to submit with files parameter
        response = client.create_task(task_request, files=[test_data_path])

        # Verify task was accepted
        assert response is not None, "Task submission returned None"

        # Response is the task_id directly
        task_id = str(response)
        assert task_id is not None, "task_id is None"
        assert len(task_id) > 0, "task_id is empty"

        print(f"✓ ANALYSIS task submitted: {task_id}")

        # Save task_id for monitoring
        with open("output/phase1_results/submitted_jobs.txt", "a") as f:
            f.write(f"ANALYSIS: {task_id}\n")

    except Exception as e:
        pytest.fail(f"ANALYSIS task submission failed: {e}")


def test_precedent_job_submits():
    """Can we submit a PRECEDENT job?"""
    from edison_client import EdisonClient, JobNames, TaskRequest

    client = EdisonClient(api_key=os.getenv("EDISON_API_KEY"))

    try:
        task_request = TaskRequest(
            name=JobNames.PRECEDENT,
            query="Has anyone developed mRNA vaccines for cancer?"
        )

        response = client.create_task(task_request)

        # Verify task was accepted
        assert response is not None, "Task submission returned None"

        # Response is the task_id directly
        task_id = str(response)
        assert task_id is not None, "task_id is None"
        assert len(task_id) > 0, "task_id is empty"

        print(f"✓ PRECEDENT task submitted: {task_id}")

        # Save task_id for monitoring
        with open("output/phase1_results/submitted_jobs.txt", "a") as f:
            f.write(f"PRECEDENT: {task_id}\n")

    except Exception as e:
        pytest.fail(f"PRECEDENT task submission failed: {e}")


def test_molecules_job_submits():
    """Can we submit a MOLECULES job?"""
    from edison_client import EdisonClient, JobNames, TaskRequest

    client = EdisonClient(api_key=os.getenv("EDISON_API_KEY"))

    try:
        task_request = TaskRequest(
            name=JobNames.MOLECULES,
            query="Predict ADMET properties for aspirin (SMILES: CC(=O)Oc1ccccc1C(=O)O)"
        )

        response = client.create_task(task_request)

        # Verify task was accepted
        assert response is not None, "Task submission returned None"

        # Response is the task_id directly
        task_id = str(response)
        assert task_id is not None, "task_id is None"
        assert len(task_id) > 0, "task_id is empty"

        print(f"✓ MOLECULES task submitted: {task_id}")

        # Save task_id for monitoring
        with open("output/phase1_results/submitted_jobs.txt", "a") as f:
            f.write(f"MOLECULES: {task_id}\n")

    except Exception as e:
        pytest.fail(f"MOLECULES task submission failed: {e}")
