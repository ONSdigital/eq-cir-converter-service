"""Tests for the schema processor service."""

from collections.abc import Mapping
from typing import Any, cast

import pytest

from eq_cir_converter_service.services.schema.schema_processor_service import (
    transform_json_schema,
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
    ],
)
def test_transform_json_schema_basic_cases(data, paths, expected):
    """Test basic JSON transformation cases."""
    result = transform_json_schema(data, paths)
    assert result == expected


@pytest.mark.parametrize(
    "data, paths, expected_placeholders_count, expected_length",
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
    data: dict, paths: list[str], expected_placeholders_count: list[int], expected_length: int,
):
    """Test transformation of a JSON object with text and placeholders."""
    result = transform_json_schema(data, paths)

    result = cast(Mapping[str, Any], result)
    desc = result["question"]["description"]
    assert len(desc) == expected_length
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


def test_transform_json_schema_with_mixed_types(placeholder_obj):
    """Test transformation of a JSON object with mixed types."""
    data = {
        "items": [
            "Simple <b>value</b>",
            {"text": "<p>Hi {first_name}</p>", "placeholders": [placeholder_obj]},
            {"info": "<p>Info1</p><p>Info2</p>"},
        ],
    }
    paths = ["items[*]"]
    result = transform_json_schema(data, paths)

    assert isinstance(result["items"], list)
    assert result["items"][0] == "Simple <strong>value</strong>"

    text_objs = [x for x in result["items"] if isinstance(x, dict) and "text" in x]
    assert any(obj["text"] == "Hi {first_name}" for obj in text_objs)

    info_objs = [x for x in result["items"] if isinstance(x, dict) and "info" in x]
    assert len(info_objs) == 1
    assert info_objs[0]["info"] == ["Info1", "Info2"]


def test_transform_json_schema_bad_types():
    """Test transformation with bad types."""
    data = {"items": [123, None, True, {"text": "<p>Test</p>"}]}
    paths = ["items[*]"]
    result = transform_json_schema(data, paths)

    assert isinstance(result["items"], list)
    assert result["items"] == [123, None, True, "Test"]


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
    result = transform_json_schema(data, paths)

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
