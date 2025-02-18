"""This module contains the unit tests for the schema router."""

from fastapi import status
from fastapi.testclient import TestClient


def test_schema_router_with_valid_json(test_client: TestClient) -> None:
    """Test the post schema method with valid JSON."""
    response = test_client.post(
        "/schema?current_version=9.0.0&target_version=10.0.0",
        json={"valid_json": "valid_json"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["valid_json"] == "valid_json"


def test_schema_router_with_invalid_current_version(test_client: TestClient) -> None:
    """Test the post schema method with invalid current version."""
    response = test_client.post(
        "/schema?current_version=1&target_version=2",
        json={"valid_json": "valid_json"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"status": "error", "message": "Invalid current version received"}


def test_schema_router_with_invalid_target_version(test_client: TestClient) -> None:
    """Test the post schema method with invalid target version."""
    response = test_client.post(
        "/schema?current_version=9.0.0&target_version=2",
        json={"valid_json": "valid_json"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"status": "error", "message": "Invalid target version received"}


def test_schema_router_with_current_version_pattern_match(test_client: TestClient) -> None:
    """Test the post schema method with invalid target version."""
    response = test_client.post(
        "/schema?current_version=1.0.0&target_version=2",
        json={"valid_json": "valid_json"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"status": "error", "message": "Invalid current version received"}


def test_schema_router_with_target_version_pattern_match(test_client: TestClient) -> None:
    """Test the post schema method with invalid target version."""
    response = test_client.post(
        "/schema?current_version=9.0.0&target_version=2.0.0",
        json={"valid_json": "valid_json"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"status": "error", "message": "Invalid target version received"}


def test_schema_router_with_empty_json(test_client: TestClient) -> None:
    """Test the post schema method with empty JSON."""
    response = test_client.post(
        "/schema?current_version=9.0.0&target_version=10.0.0",
        json={},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"status": "error", "message": "Input JSON schema is empty"}


def test_schema_router_to_simulate_processing_exception(test_client: TestClient) -> None:
    """Test the post schema method with empty JSON."""
    response = test_client.post(
        "/schema?current_version=9.0.0&target_version=10.0.0",
        json={"simulate_processing_exception": "simulate_processing_exception"},
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"status": "error", "message": "Error encountered while processing the schema"}
