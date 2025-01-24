"""Configuration for unit tests."""

from collections.abc import Generator

import app.main as app
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    """General client for hitting endpoints in tests."""
    yield TestClient(app.app)
