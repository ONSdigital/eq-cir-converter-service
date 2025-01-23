"""Configuration for unit tests."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

import app.main as app


@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    """General client for hitting endpoints in tests."""
    yield TestClient(app.app)
