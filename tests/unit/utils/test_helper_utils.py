"""Pytest unit tests for text utility functions."""

import pytest

from eq_cir_converter_service.utils.helper_utils import (
    clean_text,
    replace_b_with_strong,
    split_paragraphs,
)


@pytest.mark.parametrize(
    "html_text, expected",
    [
        ("<p>Hello <b>World</b></p><br><p>Second</p>", "Hello <strong>World</strong>Second"),
        ("<b>Test</b>", "<strong>Test</strong>"),
        ("<p>Only text</p>", "Only text"),
    ],
)
def test_clean_text(html_text, expected):
    """Test cleaning of HTML text."""
    assert clean_text(html_text) == expected


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("<b>bold</b> and <B>also</B>", "<strong>bold</strong> and <strong>also</strong>"),
        ("no bold tags", "no bold tags"),
    ],
)
def test_replace_b_with_strong(input_text, expected):
    """Test replacing <b> and </b> tags with <strong> equivalents."""
    assert replace_b_with_strong(input_text) == expected


@pytest.mark.parametrize(
    "html_text, expected",
    [
        ("<p>One</p><p>Two <b>bold</b></p><p>Three</p>", ["One", "Two <b>bold</b>", "Three"]),
        ("<p>Alpha</p><p>Beta</p>", ["Alpha", "Beta"]),
    ],
)
def test_split_paragraphs(html_text, expected):
    """Test splitting HTML text into paragraph strings."""
    assert split_paragraphs(html_text) == expected
