"""This module contains the unit tests for the schema router."""

from unittest.mock import patch

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from eq_cir_converter_service.exception import exception_messages

DEFAULT_CURRENT_VERSION = "9.0.0"
DEFAULT_TARGET_VERSION = "10.0.0"
DEFAULT_RESPONSE_JSON = {"valid_json": "valid_json"}


@pytest.mark.parametrize(
    "current_version, target_version, actual_response_json, expected_response_json, expected_status_code",
    [
        # Test the post schema method with valid JSON
        (
            DEFAULT_CURRENT_VERSION,
            DEFAULT_TARGET_VERSION,
            DEFAULT_RESPONSE_JSON,
            DEFAULT_RESPONSE_JSON,
            status.HTTP_200_OK,
        ),
        # Test the post schema method with invalid current version
        (
            "1",
            DEFAULT_TARGET_VERSION,
            DEFAULT_RESPONSE_JSON,
            {
                "detail": {"status": "error", "message": exception_messages.exception_400_invalid_version("current")},
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        # Test the post schema method with invalid target version
        (
            DEFAULT_CURRENT_VERSION,
            "2",
            DEFAULT_RESPONSE_JSON,
            {
                "detail": {"status": "error", "message": exception_messages.exception_400_invalid_version("target")},
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        # Test the post schema method with empty JSON
        (
            DEFAULT_CURRENT_VERSION,
            DEFAULT_TARGET_VERSION,
            {},
            {
                "detail": {"status": "error", "message": exception_messages.EXCEPTION_400_EMPTY_INPUT_JSON},
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        # Test the post schema method with current version and target version equal
        (
            DEFAULT_CURRENT_VERSION,
            DEFAULT_CURRENT_VERSION,  # Uses same value for both current and target version
            DEFAULT_RESPONSE_JSON,
            {
                "detail": {"status": "error", "message": exception_messages.EXCEPTION_400_MATCHING_SCHEMA_VERSIONS},
            },
            status.HTTP_400_BAD_REQUEST,
        ),
    ],
)
def test_schema_router_post(
    test_client: TestClient,
    current_version: str,
    target_version: str,
    actual_response_json: object,
    expected_response_json: object,
    expected_status_code: int,
) -> None:
    """Test the post schema method."""
    response = test_client.post(
        f"/schema?current_version={current_version}&target_version={target_version}",
        json=actual_response_json,
    )
    assert response.status_code == expected_status_code
    assert response.json() == expected_response_json


def test_convert_schema_http_exception(test_client: TestClient) -> None:
    """Test the convert schema method with an HTTPException."""
    with patch(
        "eq_cir_converter_service.services.schema.schema_processor_service.convert_schema",
        side_effect=HTTPException(status_code=400, detail="Mocked HTTPException"),
    ) as mock_convert_schema:
        response = test_client.post(
            f"/schema?current_version={DEFAULT_CURRENT_VERSION}&target_version={DEFAULT_TARGET_VERSION}",
            json=DEFAULT_RESPONSE_JSON,
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {
            "detail": {"status": "error", "message": exception_messages.EXCEPTION_500_SCHEMA_PROCESSING},
        }

        mock_convert_schema.assert_called_with(
            DEFAULT_CURRENT_VERSION,
            DEFAULT_TARGET_VERSION,
            DEFAULT_RESPONSE_JSON,
        )
