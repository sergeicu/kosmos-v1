"""Reusable Edison client wrapper for Kosmos experiments.

This wrapper simplifies interaction with the Edison API for all 4 Kosmos job types:
- LITERATURE: Literature search and synthesis
- ANALYSIS: Data analysis tasks
- PRECEDENT: Precedent search
- MOLECULES: Molecular property prediction

Usage:
    from edison_wrapper import KosmosClient

    client = KosmosClient()  # Uses EDISON_API_KEY from .env
    task_id = client.submit_literature("What is CRISPR-Cas9?")
    print(f"Task submitted: {task_id}")
"""

import os
from dotenv import load_dotenv
from edison_client import EdisonClient, JobNames, TaskRequest

load_dotenv()


class KosmosClient:
    """Wrapper for Edison API with Kosmos-specific methods."""

    def __init__(self, api_key=None):
        """
        Initialize Kosmos client.

        Args:
            api_key: Edison API key. If None, reads from EDISON_API_KEY env variable.
        """
        self.api_key = api_key or os.getenv("EDISON_API_KEY")
        if not self.api_key:
            raise ValueError("EDISON_API_KEY not found in environment or provided")
        self.client = EdisonClient(api_key=self.api_key)

    def submit_literature(self, query: str) -> str:
        """
        Submit a LITERATURE task.

        Args:
            query: Research question or literature search query

        Returns:
            task_id: UUID string of submitted task

        Example:
            task_id = client.submit_literature("What is CRISPR-Cas9?")
        """
        task_request = TaskRequest(
            name=JobNames.LITERATURE,
            query=query
        )
        return str(self.client.create_task(task_request))

    def submit_analysis(self, query: str, files: list[str] = None) -> str:
        """
        Submit an ANALYSIS task with optional data files.

        Args:
            query: Analysis question or description
            files: List of file paths to upload (CSV, TSV, etc.)

        Returns:
            task_id: UUID string of submitted task

        Example:
            task_id = client.submit_analysis(
                "Describe this dataset",
                files=["data/experiment.csv"]
            )
        """
        task_request = TaskRequest(
            name=JobNames.ANALYSIS,
            query=query
        )
        return str(self.client.create_task(task_request, files=files))

    def submit_precedent(self, query: str) -> str:
        """
        Submit a PRECEDENT search task.

        Args:
            query: Precedent search query

        Returns:
            task_id: UUID string of submitted task

        Example:
            task_id = client.submit_precedent(
                "Has anyone developed mRNA vaccines for cancer?"
            )
        """
        task_request = TaskRequest(
            name=JobNames.PRECEDENT,
            query=query
        )
        return str(self.client.create_task(task_request))

    def submit_molecules(self, query: str) -> str:
        """
        Submit a MOLECULES prediction task.

        Args:
            query: Molecular query (can include SMILES strings)

        Returns:
            task_id: UUID string of submitted task

        Example:
            task_id = client.submit_molecules(
                "Predict ADMET properties for aspirin (SMILES: CC(=O)Oc1ccccc1C(=O)O)"
            )
        """
        task_request = TaskRequest(
            name=JobNames.MOLECULES,
            query=query
        )
        return str(self.client.create_task(task_request))

    def get_task(self, task_id: str):
        """
        Get task status and results.

        Args:
            task_id: UUID string of task

        Returns:
            Task response object with status and results

        Example:
            task = client.get_task(task_id)
            print(task.status)
        """
        return self.client.get_task(task_id)

    def get_tasks(self, **kwargs):
        """
        List tasks with optional filters.

        Args:
            **kwargs: Filter parameters (project_id, status, etc.)

        Returns:
            List of task objects

        Example:
            tasks = client.get_tasks()
            for task in tasks:
                print(f"{task.task_id}: {task.status}")
        """
        return self.client.get_tasks(**kwargs)

    def cancel_task(self, task_id: str):
        """
        Cancel a running task.

        Args:
            task_id: UUID string of task to cancel

        Returns:
            Response from cancel operation

        Example:
            client.cancel_task(task_id)
        """
        return self.client.cancel_task(task_id)
