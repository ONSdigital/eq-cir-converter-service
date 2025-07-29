import json
from fastapi.testclient import TestClient
from pathlib import Path

DEFAULT_CURRENT_VERSION = "9.0.0"
DEFAULT_TARGET_VERSION = "10.0.0"

def test_schema_transformation_matches_expected_output(test_client: TestClient):
    # Load test input and expected output
    input_file_path = "tests/integration/input_schema.json"
    output_file_path = "tests/integration/output_schema.json"

    input_schema = json.loads(Path(input_file_path).read_text(encoding="utf-8"))

    expected_output = json.loads(Path(output_file_path).read_text(encoding="utf-8"))

    # Make POST request to the transformation endpoint
    response = test_client.post(
    f"/schema?current_version={DEFAULT_CURRENT_VERSION}&target_version={DEFAULT_TARGET_VERSION}",
    json=input_schema,
    )

    assert response.status_code == 200, "Response failed with non-200 status"
    transformed_output = response.json()

    assert transformed_output == expected_output, "Transformed schema did not match expected output"
