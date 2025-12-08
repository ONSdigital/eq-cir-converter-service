"""Tests for helper utilities."""

from collections.abc import Mapping
from typing import Any, cast

import pytest

from eq_cir_converter_service.converters.v10 import (
    convert_to_v10,
    extract_placeholder_names_from_text_field,
    get_sanitised_text,
    process_item,
    process_list,
    process_placeholder,
    process_string,
    split_paragraphs_into_list,
    split_paragraphs_with_placeholders,
)


@pytest.mark.parametrize(
    "data, paths, expected",
    [
        (
            {"contents": [{"description": "<p>Block1</p><p>Block2</p>"}]},
            ["contents[*].description"],
            {"contents": [{"description": ["Block1", "Block2"]}]},
        ),
        (
            {"contents": [{"description": ["<p>Block1</p>", "<p>Block2</p>"]}]},
            ["contents[*].description"],
            {"contents": [{"description": ["Block1", "Block2"]}]},
        ),
        (
            {"contents": [{"description": ["<p>Block1</p></p><p>", "<p>Block2</p>"]}]},
            ["contents[*].description"],
            {"contents": [{"description": ["Block1", "Block2"]}]},
        ),
        (
            {"contents": [{"description": "<p>Block1</p><p>Block2</p><p>Block3</p><p>"}]},
            ["contents[*].description"],
            {"contents": [{"description": ["Block1", "Block2", "Block3"]}]},
        ),
        (
            {"contents": [{"description": "<p><p>Block1</p><p>Block2</p><p></p><p>"}]},
            ["contents[*].description"],
            {"contents": [{"description": ["Block1", "Block2"]}]},
        ),
        (
            {"meta": {"notes": "<p>Alpha</p><p>Beta</p>"}},
            ["meta.notes"],
            {"meta": {"notes": ["Alpha", "Beta"]}},
        ),
        (
            {"meta": {"notes": "<p>Alpha</p><b>Beta</b>"}},
            ["meta.notes"],
            {"meta": {"notes": "Alpha"}},
        ),
        (
            {"meta": {"notes": "<p>Alpha</p><strong>Beta</strong>"}},
            ["meta.notes"],
            {"meta": {"notes": "Alpha"}},
        ),
        (
            {"meta": {"notes": "<strong>Alpha</strong>"}},
            ["meta.notes"],
            {"meta": {"notes": "<strong>Alpha</strong>"}},
        ),
        (
            {"meta": {"notes": "<b>Alpha</b>"}},
            ["meta.notes"],
            {"meta": {"notes": "<strong>Alpha</strong>"}},
        ),
        (
            {"meta": {"notes": "<p></p>"}},
            ["meta.notes"],
            {"meta": {"notes": []}},
        ),
    ],
)
def test_transform_json_schema_basic_cases(data, paths, expected):
    """Test basic JSON transformation cases."""
    result = convert_to_v10(data, paths)
    assert result == expected


@pytest.mark.parametrize(
    "data, paths, expected_placeholders_count, expected_paragraphs_count",
    [
        (
            {
                "question": {
                    "description": [
                        {
                            "text": "<p>Hello {first_name}</p><p>Welcome again {first_name}</p>",
                            "placeholders": [
                                {
                                    "placeholder": "first_name",
                                    "value": {"source": "metadata", "identifier": "FIRST_NAME"},
                                },
                            ],
                        },
                    ],
                },
            },
            ["question.description[*]"],
            [1, 1],
            2,
        ),
        (
            {
                "question": {
                    "description": [
                        {
                            "text": "<p>Hello {first_name} {last_name}</p>",
                            "placeholders": [
                                {
                                    "placeholder": "first_name",
                                    "value": {"source": "metadata", "identifier": "FIRST_NAME"},
                                },
                                {
                                    "placeholder": "last_name",
                                    "value": {"source": "metadata", "identifier": "LAST_NAME"},
                                },
                            ],
                        },
                    ],
                },
            },
            ["question.description[*]"],
            [2],
            1,
        ),
        (
            {
                "question": {
                    "description": [
                        {
                            "text": "<p>Hello {first_name}</p><p>Your last name is {last_name}</p>",
                            "placeholders": [
                                {
                                    "placeholder": "first_name",
                                    "value": {"source": "metadata", "identifier": "FIRST_NAME"},
                                },
                                {
                                    "placeholder": "last_name",
                                    "value": {"source": "metadata", "identifier": "LAST_NAME"},
                                },
                            ],
                        },
                    ],
                },
            },
            ["question.description[*]"],
            [1, 1],
            2,
        ),
        (
            {
                "question": {
                    "description": [
                        {
                            "text": "<p>Hello {first_name}</p><p>Your last name is {last_name}</p><p>Once again</p>"
                            "<p>Your first name is {first_name}</p><p>Your last name is {last_name}</p>",
                            "placeholders": [
                                {
                                    "placeholder": "first_name",
                                    "value": {"source": "metadata", "identifier": "FIRST_NAME"},
                                },
                                {
                                    "placeholder": "last_name",
                                    "value": {"source": "metadata", "identifier": "LAST_NAME"},
                                },
                            ],
                        },
                    ],
                },
            },
            ["question.description[*]"],
            [1, 1, 0, 1, 1],
            5,
        ),
        (
            {
                "question": {
                    "description": [
                        {
                            "text": "<p><p>Hello {first_name} {last_name}</p></p></p>",
                            "placeholders": [
                                {
                                    "placeholder": "first_name",
                                    "value": {"source": "metadata", "identifier": "FIRST_NAME"},
                                },
                                {
                                    "placeholder": "last_name",
                                    "value": {"source": "metadata", "identifier": "LAST_NAME"},
                                },
                            ],
                        },
                    ],
                },
            },
            ["question.description[*]"],
            [2],
            1,
        ),
    ],
)
def test_transform_json_schema_with_text_object_and_placeholders(
    data: dict,
    paths: list[str],
    expected_placeholders_count: list[int],
    expected_paragraphs_count: int,
):
    """Test transformation of a JSON object with text and placeholders."""
    result = convert_to_v10(data, paths)

    result = cast(Mapping[str, Any], result)
    desc = cast(Mapping[str, Any], result)["question"]["description"]
    assert len(desc) == expected_paragraphs_count
    expected_texts = []
    for item in desc:
        if isinstance(item, dict) and "text" in item:
            expected_texts.append(item["text"])
        else:
            expected_texts.append(item)

    for i, expected_text in enumerate(expected_texts):
        if isinstance(desc[i], str):
            assert desc[i] == expected_text
        else:
            assert desc[i]["text"] == expected_text
            assert len(desc[i]["placeholders"]) == expected_placeholders_count[i]


def test_transform_json_schema_with_mixed_types(placeholder_object):
    """Test transformation of a JSON object with mixed types."""
    data = {
        "items": [
            "Simple <b>value</b>",
            {"text": "<p>Hi {first_name}</p>", "placeholders": [placeholder_object]},
            {"info": "<p>Info1</p><p>Info2</p>"},
        ],
    }
    paths = ["items[*]"]
    result = convert_to_v10(data, paths)

    assert isinstance(result["items"], list)
    assert result["items"][0] == "Simple <strong>value</strong>"

    text_objects = [x for x in result["items"] if isinstance(x, dict) and "text" in x]
    assert any(obj["text"] == "Hi {first_name}" for obj in text_objects)

    info_objects = [x for x in result["items"] if isinstance(x, dict) and "info" in x]
    assert len(info_objects) == 1
    assert info_objects[0]["info"] == ["Info1", "Info2"]


@pytest.mark.parametrize(
    "input_data",
    [
        {"items": [123, {"text": "<p>Test</p>"}]},
        {"items": [None, {"text": "<p>Test</p>"}]},
        {"items": [True, {"text": "<p>Test</p>"}]},
    ],
)
def test_transform_json_schema_bad_types(input_data):
    """Test transformation with bad types and raw types."""
    with pytest.raises(TypeError):
        convert_to_v10({"items": input_data}, ["items[*]"])


def test_transform_json_schema_placeholder_with_multiple_paragraphs_description():
    """Test transformation of a JSON object with a placeholder and multiple paragraphs."""
    data = {
        "question": {
            "description": [
                {
                    "text": "<p>Your first name: {first_name}</p><p>Your last name: {last_name}</p>",
                    "placeholders": [
                        {
                            "placeholder": "first_name",
                            "value": {"source": "answers", "identifier": "first-name"},
                        },
                        {"placeholder": "last_name", "value": {"source": "answers", "identifier": "last-name"}},
                    ],
                },
            ],
        },
    }
    paths = ["question.description[*]"]
    result = convert_to_v10(data, paths)

    assert result == {
        "question": {
            "description": [
                {
                    "text": "Your first name: {first_name}",
                    "placeholders": [
                        {"placeholder": "first_name", "value": {"source": "answers", "identifier": "first-name"}},
                    ],
                },
                {
                    "text": "Your last name: {last_name}",
                    "placeholders": [
                        {"placeholder": "last_name", "value": {"source": "answers", "identifier": "last-name"}},
                    ],
                },
            ],
        },
    }


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
    assert get_sanitised_text(input_html) == expected


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


def test_split_text_with_placeholders_single(placeholder_object):
    """Test splitting text with a single placeholder."""
    input_object = {"text": "<p>Hello {first_name}</p>", "placeholders": [placeholder_object]}
    result = split_paragraphs_with_placeholders(input_object)
    assert len(result) == 1
    assert isinstance(result[0], dict)
    assert "text" in result[0]
    assert "placeholders" in result[0]
    assert result[0]["text"] == "Hello {first_name}"
    assert result[0]["placeholders"] == [placeholder_object]


def test_split_text_with_placeholders_multiple(placeholder_object):
    """Test splitting text with multiple paragraphs and placeholders."""
    input_object = {"text": "<p>Hi {first_name}</p><p>Again {first_name}</p>", "placeholders": [placeholder_object]}
    result = split_paragraphs_with_placeholders(input_object)
    assert len(result) == 2
    for item in result:
        assert isinstance(item, dict)
        assert "placeholders" in item
        assert item["placeholders"] == [placeholder_object]


@pytest.mark.parametrize(
    "text,expected",
    [
        ("<p>One</p><p>Two</p>", ["One", "Two"]),
        ("<p></p><p>Second</p>", "Second"),
        ("No tags", "No tags"),
        ("<p>  </p><p>Second</p>", "Second"),
        ("<p><p>First</p></p>", "First"),
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


def test_process_text_object_with_paragraphs(placeholder_object):
    """Test processing a text object with paragraphs and placeholders."""
    input_object = {
        "text": "<p>Welcome {first_name}</p><p>Again {first_name}</p>",
        "placeholders": [placeholder_object],
    }
    result = process_placeholder(input_object)
    assert len(result) == 2
    assert all("text" in item for item in result)


def test_process_text_object_without_paragraphs(placeholder_object):
    """Test processing a text object without paragraphs."""
    input_object = {"text": "Hello <b>{first_name}</b>", "placeholders": [placeholder_object]}
    result = process_placeholder(input_object)
    assert isinstance(result, dict)
    assert result["text"] == "Hello <strong>{first_name}</strong>"


def test_process_list_with_dict_and_string():
    """Test processing a list with a mix of dicts and strings."""
    items = [{"description": "<p>One</p><p>Two</p>"}, "Text"]
    result = process_list(items)
    assert result == [{"description": "One"}, {"description": "Two"}, "Text"]


def test_process_element_string():
    """Test processing a simple string."""
    assert process_item("<p>Test</p>") == "Test"
    assert process_item("Simple") == "Simple"


def test_process_element_text_object(placeholder_object):
    """Test processing a text object with placeholders."""
    input_object = {"text": "<p>Hello {first_name}</p>", "placeholders": [placeholder_object]}
    result = process_item(input_object)
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], dict)
    assert "text" in result[0]
    assert result[0]["text"] == "Hello {first_name}"


def test_process_element_list(placeholder_object):
    """Test processing a list with mixed content."""
    data = [
        {"description": "<p>Item1</p><p>Item2</p>"},
        "Some text",
        {"text": "<p>With {first_name}</p>", "placeholders": [placeholder_object]},
    ]
    result = process_item(data)

    assert isinstance(result, list)
    assert result[0] == {"description": "Item1"}
    assert result[1] == {"description": "Item2"}
    assert result[2] == "Some text"
    assert result[3]["text"] == "With {first_name}"


def test_process_element_dict():
    """Test processing a dictionary with mixed content."""
    input_object = {"a": "<p>One</p>", "b": "plain"}
    result = process_item(input_object)
    assert result == {"a": "One", "b": "plain"}


def test_split_text_with_placeholders_empty_paragraph_skipped():
    """Test that empty paragraphs are skipped in the output."""
    input_object = {"text": "<p></p><p>Hello</p>", "placeholders": []}
    result = split_paragraphs_with_placeholders(input_object)
    assert result == ["Hello"]


def test_split_text_with_placeholders_no_placeholders():
    """Test splitting text with no placeholders."""
    input_object = {"text": "<p>Hello world</p>", "placeholders": []}
    result = split_paragraphs_with_placeholders(input_object)
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
    assert process_item(input_data) == expected


def test_process_strings_in_complex_objects():
    """Test processing a list of strings."""
    input_data = {
        "type": "List",
        "for_list": "additional_units",
        "title": "What is the name, address, and postcode of the new unit?",
        "item_anchor_answer_id": "answer27f27859-fc11-4577-b9bb-745407356498",
        "item_label": "<p>Name of new unit</p>",
        "add_link_text": "Add item to this list",
        "empty_list_text": "There are no items",
    }
    expected = {
        "type": "List",
        "for_list": "additional_units",
        "title": "What is the name, address, and postcode of the new unit?",
        "item_anchor_answer_id": "answer27f27859-fc11-4577-b9bb-745407356498",
        "item_label": "Name of new unit",
        "add_link_text": "Add item to this list",
        "empty_list_text": "There are no items",
    }
    assert process_item(input_data) == expected
