"""This module contains the unit tests for the schema router."""

from unittest.mock import MagicMock

from fastapi import status
from fastapi.testclient import TestClient

from eq_cir_converter_service.exception.exception_response_models import (
    exception_400_empty_input_json,
    exception_400_invalid_current_version,
    exception_400_invalid_target_version,
)
from eq_cir_converter_service.exception.exceptions import SchemaProcessingException
from eq_cir_converter_service.services.schema.schema_processor_service import SchemaProcessorService

current_version = "9.0.0"
target_version = "10.0.0"


def test_schema_router_with_valid_json(test_client: TestClient) -> None:
    """Test the post schema method with valid JSON."""
    response = test_client.post(
        f"/schema?current_version={current_version}&target_version={target_version}",
        json={"valid_json": "valid_json"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["valid_json"] == "valid_json"


def test_schema_router_with_invalid_current_version(test_client: TestClient) -> None:
    """Test the post schema method with invalid current version."""
    response = test_client.post(
        f"/schema?current_version=1&target_version={target_version}",
        json={"valid_json": "valid_json"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"status": "error", "message": exception_400_invalid_current_version.message}


def test_schema_router_with_invalid_target_version(test_client: TestClient) -> None:
    """Test the post schema method with invalid target version."""
    response = test_client.post(
        f"/schema?current_version={current_version}&target_version=2",
        json={"valid_json": "valid_json"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"status": "error", "message": exception_400_invalid_target_version.message}


def test_schema_router_with_empty_json(test_client: TestClient) -> None:
    """Test the post schema method with empty JSON."""
    response = test_client.post(
        f"/schema?current_version={current_version}&target_version={target_version}",
        json={},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"status": "error", "message": exception_400_empty_input_json.message}


def test_convert_schema_exception(test_client: TestClient) -> None:
    """Test convert_schema method to raise SchemaProcessingException."""
    SchemaProcessorService.convert_schema = MagicMock(side_effect=SchemaProcessingException("Test Exception"))
    response = test_client.post(
        f"/schema?current_version={current_version}&target_version={target_version}",
        json={"valid_json": "valid_json"},
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"status": "error", "message": "Error encountered while processing the schema"}
    SchemaProcessorService.convert_schema.assert_called_with(
        current_version, target_version, {"valid_json": "valid_json"}
    )
