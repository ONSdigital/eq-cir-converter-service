"""Unit tests for text utility functions."""

import unittest

from eq_cir_converter_service.utils.text_utils import clean_text, replace_b_with_strong, split_paragraphs


class TestTextUtils(unittest.TestCase):
    """These tests cover the text utility functions.

    This includes the cleaning of HTML text, the replacement of <b> tags with <strong> tags,
    and the splitting of text into paragraphs.
    """

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
