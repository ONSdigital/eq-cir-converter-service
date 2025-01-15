import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def test_client():
    """General client for hitting endpoints in tests."""
    import src.main as app

    test_client = TestClient(app.app)
    yield test_client
