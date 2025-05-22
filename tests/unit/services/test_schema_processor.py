"""Unit tests for the schema processor service."""

import unittest

from eq_cir_converter_service.services.schema.schema_processor_service import (
    process_description,
    transform_json,
)


class TestSchemaProcessorService(unittest.TestCase):
    """These tests cover the schema processor service.

    This includes the transformation of JSON data and the processing of description fields.
    """

    def test_process_description_string_passthrough(self):
        """Test the processing of a description with a string input."""
        result = process_description(["Simple string"])
        self.assertEqual(result, ["Simple string"])

    def test_transform_json_recursive(self):
        """Test the recursive transformation of JSON data."""
        sample = {
            "description": [
                {
                    "text": "<p>Please note: what constitutes a &#x2018;significant change&#x2019; is dependent on "
                    "your own interpretation in relation to {trad_as}&#x2019;s figures from the previous reporting "
                    "period and the same reporting period last year.</p><p>This information will help us to validate "
                    "your data and should reduce the need to query any figures with you.</p>",
                    "placeholders": [
                        {
                            "placeholder": "trad_as",
                            "transforms": [
                                {
                                    "transform": "first_non_empty_item",
                                    "arguments": {
                                        "items": [
                                            {"source": "metadata", "identifier": "trad_as"},
                                            {"source": "metadata", "identifier": "ru_name"},
                                        ],
                                    },
                                },
                            ],
                        },
                    ],
                },
            ],
            "nested": {"html": "<b>Bold</b>", "list": ["<b>item1</b>", "item2"]},
        }

        transformed = transform_json(sample)

        self.assertEqual(
            transformed["description"][0]["text"],
            "Please note: what constitutes a &#x2018;significant change&#x2019; is dependent on your own "
            "interpretation in relation to {trad_as}&#x2019;s figures from the previous reporting period and the same "
            "reporting period last year.",
        )
        self.assertEqual(
            transformed["description"][1],
            "This information will help us to validate your data and should reduce the need to query any "
            "figures with you.",
        )
        self.assertEqual(transformed["nested"]["html"], "<strong>Bold</strong>")
        self.assertEqual(transformed["nested"]["list"][0], "<strong>item1</strong>")
        self.assertEqual(transformed["nested"]["list"][1], "item2")
