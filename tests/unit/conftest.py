import pytest
from fastapi.testclient import TestClient

import src.main as app


@pytest.fixture
def test_client():
    """General client for hitting endpoints in tests."""
    yield TestClient(app.app)
