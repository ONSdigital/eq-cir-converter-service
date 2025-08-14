"""Integration tests for schema transformation."""

import json

from fastapi.testclient import TestClient

DEFAULT_CURRENT_VERSION = "9.0.0"
DEFAULT_TARGET_VERSION = "10.0.0"


def test_schema_transformation_matches_expected_output(test_client: TestClient):
    """Test that the schema transformation endpoint returns the expected output."""
    # Define the input and output file paths
    input_file_path = "tests/integration/input_schema.json"
    output_file_path = "tests/integration/output_schema.json"

    # Load input JSON
    with open(input_file_path, encoding="utf-8") as f:
        input_schema = json.load(f)

    # Load expected output JSON
    with open(output_file_path, encoding="utf-8") as f:
        expected_output = json.load(f)

    # Make POST request to the transformation endpoint
    response = test_client.post(
        f"/schema?current_version={DEFAULT_CURRENT_VERSION}&target_version={DEFAULT_TARGET_VERSION}",
        json=input_schema,
    )

    assert response.status_code == 200, "Response failed with non-200 status"
    transformed_output = response.json()

    assert transformed_output == expected_output, "Transformed schema did not match expected output"
