"""Tests for helper utilities."""

import pytest

from eq_cir_converter_service.utils.helper_utils import (
    extract_placeholder_names_from_text_field,
    process_element,
    process_list,
    process_placeholder,
    process_string,
    remove_and_replace_tags,
    split_paragraphs_into_list,
    split_text_with_placeholders,
)


@pytest.mark.parametrize(
    "input_html,expected",
    [
        ("<b>bold</b>", "<strong>bold</strong>"),
        ("<p>text</p>", "text"),
        ("<br>", ""),
        ("<b>bold</b><p>test</p><br>", "<strong>bold</strong>test"),
    ],
)
def test_clean_html_tags(input_html, expected):
    """Test the clean_html_tags function."""
    assert remove_and_replace_tags(input_html) == expected


@pytest.mark.parametrize(
    "paragraphs_string,expected",
    [
        ("<p>One</p>", ["One"]),
        ("<p>One</p><p>Two</p>", ["One", "Two"]),
        ("<p>One</p></p><p>Two</p>", ["One", "Two"]),
        ("<p></p><p>Another</p>", ["Another"]),
    ],
)
def test_extract_paragraphs(paragraphs_string, expected):
    """Test the extract_paragraphs function."""
    assert split_paragraphs_into_list(paragraphs_string) == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Hello {name}", ["name"]),
        ("No placeholders here", []),
        ("{a} and {b} and {a}", ["a", "b", "a"]),
    ],
)
def test_extract_placeholders(text, expected):
    """Test the extract_placeholders function."""
    assert extract_placeholder_names_from_text_field(text) == expected


def test_split_text_with_placeholders_single(placeholder_obj):
    """Test splitting text with a single placeholder."""
    input_obj = {"text": "<p>Hello {first_name}</p>", "placeholders": [placeholder_obj]}
    result = split_text_with_placeholders(input_obj)
    assert len(result) == 1
    assert isinstance(result[0], dict)
    assert "text" in result[0]
    assert "placeholders" in result[0]
    assert result[0]["text"] == "Hello {first_name}"
    assert result[0]["placeholders"] == [placeholder_obj]


def test_split_text_with_placeholders_multiple(placeholder_obj):
    """Test splitting text with multiple paragraphs and placeholders."""
    input_obj = {"text": "<p>Hi {first_name}</p><p>Again {first_name}</p>", "placeholders": [placeholder_obj]}
    result = split_text_with_placeholders(input_obj)
    assert len(result) == 2
    for item in result:
        assert isinstance(item, dict)
        assert "placeholders" in item
        assert item["placeholders"] == [placeholder_obj]


@pytest.mark.parametrize(
    "text,expected",
    [
        ("<p>One</p><p>Two</p>", ["One", "Two"]),
        ("<p></p><p>Second</p>", "Second"),
        ("No tags", "No tags"),
    ],
)
def test_process_string(text, expected):
    """Test the process_string function."""
    assert process_string(text) == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("<p>Single</p>", "Single"),
        ("<p>One</p><p>Two</p>", ["One", "Two"]),
    ],
)
def test_process_string_single_vs_multiple(input_text, expected):
    """Test processing a string that may expand to multiple paragraphs."""
    assert process_string(input_text) == expected


def test_process_text_object_with_paragraphs(placeholder_obj):
    """Test processing a text object with paragraphs and placeholders."""
    obj = {"text": "<p>Welcome {first_name}</p><p>Again {first_name}</p>", "placeholders": [placeholder_obj]}
    result = process_placeholder(obj)
    assert len(result) == 2
    assert all("text" in item for item in result)


def test_process_text_object_without_paragraphs(placeholder_obj):
    """Test processing a text object without paragraphs."""
    obj = {"text": "Plain text with <b>bold</b>", "placeholders": [placeholder_obj]}
    result = process_placeholder(obj)
    assert isinstance(result, dict)
    assert result["text"] == "Plain text with <strong>bold</strong>"


def test_process_list_with_dict_and_string():
    """Test processing a list with a mix of dicts and strings."""
    items = [{"description": "<p>One</p><p>Two</p>"}, "Text"]
    result = process_list(items)
    assert result == [{"description": "One"}, {"description": "Two"}, "Text"]


def test_process_element_string():
    """Test processing a simple string."""
    assert process_element("<p>Test</p>") == "Test"
    assert process_element("Simple") == "Simple"


def test_process_element_text_object(placeholder_obj):
    """Test processing a text object with placeholders."""
    obj = {"text": "<p>Hello {first_name}</p>", "placeholders": [placeholder_obj]}
    result = process_element(obj)
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], dict)
    assert "text" in result[0]
    assert result[0]["text"] == "Hello {first_name}"


def test_process_element_list(placeholder_obj):
    """Test processing a list with mixed content."""
    data = [
        {"description": "<p>Item1</p><p>Item2</p>"},
        "Some text",
        {"text": "<p>With {first_name}</p>", "placeholders": [placeholder_obj]},
    ]
    result = process_element(data)

    assert isinstance(result, list)
    assert {"description": "Item1"} in result
    assert {"description": "Item2"} in result
    assert "Some text" in result

    assert any(isinstance(obj, dict) and obj.get("text") == "With {first_name}" for obj in result)


def test_process_element_dict():
    """Test processing a dictionary with mixed content."""
    obj = {"a": "<p>One</p>", "b": "plain"}
    result = process_element(obj)
    assert result == {"a": "One", "b": "plain"}


def test_split_text_with_placeholders_empty_paragraph_skipped():
    """Test that empty paragraphs are skipped in the output."""
    input_obj = {"text": "<p></p><p>Hello</p>", "placeholders": []}
    result = split_text_with_placeholders(input_obj)
    assert result == ["Hello"]


def test_split_text_with_placeholders_no_placeholders():
    """Test splitting text with no placeholders."""
    input_obj = {"text": "<p>Hello world</p>", "placeholders": []}
    result = split_text_with_placeholders(input_obj)
    assert result == ["Hello world"]


def test_process_list_non_expandable_dict():
    """Test processing a list with a non-expandable dictionary."""
    data = [{"meta": "plain text"}]
    result = process_list(data)
    assert result == [{"meta": "plain text"}]


def test_process_list_string_expands_to_multiple():
    """Test processing a list with a string that expands to multiple paragraphs."""
    data = ["<p>First</p><p>Second</p>"]
    result = process_list(data)
    assert result == ["First", "Second"]


@pytest.mark.parametrize(
    "input_list,expected",
    [
        ([{"description": "<p>Only one</p>"}], [{"description": "Only one"}]),
        ([{"description": "<p>First</p><p>Second</p>"}], [{"description": "First"}, {"description": "Second"}]),
    ],
)
def test_process_list_single_vs_multiple(input_list, expected):
    """Test processing a list that may contain single or multiple paragraphs."""
    assert process_list(input_list) == expected


@pytest.mark.parametrize(
    "input_data,expected",
    [
        ("<p>Just one</p>", "Just one"),
        ("<p>First</p><p>Second</p>", ["First", "Second"]),
        ({"description": "<p>One desc</p>"}, {"description": "One desc"}),
        ({"description": "<p>First</p><p>Second</p>"}, {"description": ["First", "Second"]}),
    ],
)
def test_process_element_single_vs_multiple(input_data, expected):
    """Test processing an element that may expand to single or multiple paragraphs."""
    assert process_element(input_data) == expected


def test_process_element_returns_raw_types():
    """Test that process_element returns raw types without modification."""
    assert process_element(42) == 42
    assert process_element(None) is None
