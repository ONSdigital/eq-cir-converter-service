"""Unit tests for the schema processor service.

These tests cover the functionality of the schema processor service,
including the replacement of HTML tags, splitting paragraphs,
and processing descriptions.
"""

import unittest

from eq_cir_converter_service.services.schema.schema_processor_service import (
    clean_text,
    process_description,
    replace_b_with_strong,
    split_paragraphs,
    transform_json,
)


class TestSchemaProcessorService(unittest.TestCase):
    """Unit tests for the schema processor service."""

    def test_clean_text(self):
        """Test the cleaning of HTML text."""
        html_text = "<p>Hello <b>World</b></p><br><p>Second</p>"
        expected = "Hello <strong>World</strong>Second"
        self.assertEqual(clean_text(html_text), expected)

    def test_replace_b_with_strong(self):
        """Test the replacement of <b> and </b> tags with <strong> and </strong>."""
        self.assertEqual(
            replace_b_with_strong("<b>bold</b> and <B>also</B>"),
            "<strong>bold</strong> and <strong>also</strong>",
        )

    def test_split_paragraphs(self):
        """Test the splitting of HTML text into paragraphs."""
        html_text = "<p>One</p><p>Two <b>bold</b></p><p>Three</p>"
        expected = ["One", "Two <b>bold</b>", "Three"]
        self.assertEqual(split_paragraphs(html_text), expected)

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
