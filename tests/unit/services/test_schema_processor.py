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
            [{"json_path": "contents[*].description"}],
            {"contents": [{"description": ["Block1", "Block2"]}]},
        ),
        (
            {"meta": {"notes": "<p>Alpha</p><p>Beta</p>"}},
            [{"json_path": "meta.notes"}],
            {"meta": {"notes": ["Alpha", "Beta"]}},
        ),
    ],
)
def test_transform_json_schema_basic_cases(data, paths, expected):
    """Test basic JSON transformation cases."""
    result = transform_json_schema(data, paths)
    assert result == expected


def test_transform_json_schema_with_text_object_and_placeholders(placeholder_obj):
    """Test transformation of a JSON object with text and placeholders."""
    data = {
        "question": {
            "description": [
                {
                    "text": "<p>Hello {first_name}</p><p>Welcome again {first_name}</p>",
                    "placeholders": [placeholder_obj],
                },
            ],
        },
    }
    paths = [{"json_path": "question.description[*]"}]
    result = transform_json_schema(data, paths)

    result = cast(Mapping[str, Any], result)
    desc = result["question"]["description"]
    assert len(desc) == 2
    assert desc[0]["text"] == "Hello {first_name}"
    assert desc[1]["text"] == "Welcome again {first_name}"
    assert len(desc[0]["placeholders"]) == 1
    assert len(desc[1]["placeholders"]) == 1


def test_transform_json_schema_with_mixed_types(placeholder_obj):
    """Test transformation of a JSON object with mixed types."""
    data = {
        "items": [
            "Simple <b>value</b>",
            {"text": "<p>Hi {first_name}</p>", "placeholders": [placeholder_obj]},
            {"info": "<p>Info1</p><p>Info2</p>"},
        ],
    }
    paths = [{"json_path": "items[*]"}]
    result = transform_json_schema(data, paths)

    assert isinstance(result["items"], list)
    assert result["items"][0] == "Simple <strong>value</strong>"

    text_objs = [x for x in result["items"] if isinstance(x, dict) and "text" in x]
    assert any(obj["text"] == "Hi {first_name}" for obj in text_objs)

    info_objs = [x for x in result["items"] if isinstance(x, dict) and "info" in x]
    assert len(info_objs) == 1
    assert info_objs[0]["info"] == ["Info1", "Info2"]
