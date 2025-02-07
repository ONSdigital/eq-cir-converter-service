"""This module contains the unit tests for the schema router."""

from fastapi import status
from fastapi.testclient import TestClient


def test_schema_router_with_valid_json(test_client: TestClient) -> None:
    """Test the post schema method with valid JSON."""
    response = test_client.post(
        "/schema?current_version=1&target_version=2",
        json={"valid_json": "valid_json"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["valid_json"] == "valid_json"
