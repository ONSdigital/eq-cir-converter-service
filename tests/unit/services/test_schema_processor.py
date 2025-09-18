"""Tests for the schema processor service."""

from eq_cir_converter_service.services.schema import schema_processor


def test_convert_schema_to_v10():
    """Test converting schema to version 10.0.0."""
    result = schema_processor.process_schema(
        current_version="1.0.0",
        target_version="10.0.0",
        input_schema={
            "sections": [
                {
                    "title": "<p>Your test results</p>",
                },
            ],
        },
    )
    assert result == {"sections": [{"title": "Your test results"}]}


def test_convert_schema_no_conversion():
    """Test converting schema when no conversion is needed."""
    result = schema_processor.process_schema(
        current_version="1.0.0",
        target_version="2.0.0",
        input_schema={
            "sections": [
                {
                    "title": "<p>Your test results</p>",
                },
            ],
        },
    )
    assert result == {"sections": [{"title": "<p>Your test results</p>"}]}
