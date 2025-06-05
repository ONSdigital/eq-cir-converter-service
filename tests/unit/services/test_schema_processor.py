"""Unit tests for the schema processor service."""

import pytest

from eq_cir_converter_service.services.schema.schema_processor_service import (
    process_description,
    transform_json,
)


@pytest.mark.parametrize(
    "input_description, expected_output",
    [
        (["Simple string"], ["Simple string"]),
        (["<p>Text with HTML</p>"], ["Text with HTML"]),
        ([], []),
    ],
)
def test_process_description_varied_inputs(input_description, expected_output):
    """Test the processing of a description with varied string inputs."""
    assert process_description(input_description) == expected_output


def test_transform_json_recursive(sample_json):
    """Test recursive transformation of JSON using sample fixture."""
    transformed = transform_json(sample_json)

    assert transformed["description"][0]["text"] == (
        "Please note: what constitutes a &#x2018;significant change&#x2019; is dependent on your own "
        "interpretation in relation to {trad_as}&#x2019;s figures from the previous reporting period and the same "
        "reporting period last year."
    )
    assert transformed["description"][1] == (
        "This information will help us to validate your data and should reduce the need to query any "
        "figures with you."
    )
    assert transformed["nested"]["html"] == "<strong>Bold</strong>"
    assert transformed["nested"]["list"][0] == "<strong>item1</strong>"
    assert transformed["nested"]["list"][1] == "item2"
