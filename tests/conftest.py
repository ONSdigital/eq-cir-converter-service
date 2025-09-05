"""Configuration for unit tests."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

import eq_cir_converter_service.main as app


@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    """General client for hitting endpoints in tests."""
    yield TestClient(app.app)


@pytest.fixture
def placeholder_object():
    """Fixture to provide a sample placeholder object."""
    yield {"placeholder": "first_name", "value": {"source": "metadata", "identifier": "FIRST_NAME"}}
