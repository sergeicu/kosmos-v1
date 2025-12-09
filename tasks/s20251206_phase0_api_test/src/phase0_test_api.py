import pytest
import os
from dotenv import load_dotenv

load_dotenv()

def test_import_edison_client():
    """Can we import the Edison SDK?"""
    try:
        from edison_client import EdisonClient
        assert EdisonClient is not None
    except ImportError as e:
        pytest.fail(f"Failed to import Edison client: {e}")

def test_authenticate():
    """Can we authenticate with API key?"""
    from edison_client import EdisonClient

    api_key = os.getenv("EDISON_API_KEY")
    assert api_key is not None, "EDISON_API_KEY not set in .env file"
    assert len(api_key) > 10, "API key seems invalid (too short)"

    try:
        client = EdisonClient(api_key=api_key)
        assert client is not None
    except Exception as e:
        pytest.fail(f"Authentication failed: {e}")

def test_basic_query():
    """Can we make a simple API call?"""
    from edison_client import EdisonClient

    api_key = os.getenv("EDISON_API_KEY")
    client = EdisonClient(api_key=api_key)

    try:
        # Try listing world models as a basic read operation
        response = client.list_world_models()
        assert response is not None
        # Check response format - should be a list or dict
        assert isinstance(response, (list, dict)) or hasattr(response, '__iter__')
    except Exception as e:
        pytest.fail(f"Basic query failed: {e}")
