"""Tests for the schema processing service."""

import pytest

from eq_cir_converter_service.services.schema.schema_processor_service import transform_json


def test_transform_json_with_single_text_block():
    """Test transforming a single text block with HTML content into a list of paragraphs."""
    data = {"contents": [{"description": "<p>Block1</p><p>Block2</p>"}]}
    paths = [{"json_path": "contents[*].description"}]
    result = transform_json(data, paths)

    assert result == {"contents": [{"description": ["Block1", "Block2"]}]}


def test_transform_json_with_text_object_and_placeholders(placeholder_obj):
    """Test transforming a text object with HTML content and placeholders."""
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
    result = transform_json(data, paths)
    desc = result["question"]["description"]
    assert len(desc) == 2
    assert desc[0]["text"] == "Hello {first_name}"
    assert desc[1]["text"] == "Welcome again {first_name}"
    assert len(desc[0]["placeholders"]) == 1
    assert len(desc[1]["placeholders"]) == 1


def test_transform_json_with_string_only():
    """Test transforming a simple string without HTML tags."""
    data = {"meta": {"notes": "<p>Alpha</p><p>Beta</p>"}}
    paths = [{"json_path": "meta.notes"}]
    result = transform_json(data, paths)
    assert result == {"meta": {"notes": ["Alpha", "Beta"]}}


def test_transform_json_with_mixed_types(placeholder_obj):
    """Test transforming a mixed list with strings, text objects, and other structures."""
    data = {
        "items": [
            "Simple <b>value</b>",
            {"text": "<p>Hi {first_name}</p>", "placeholders": [placeholder_obj]},
            {"info": "<p>Info1</p><p>Info2</p>"},
        ],
    }
    paths = [{"json_path": "items[*]"}]
    result = transform_json(data, paths)

    assert isinstance(result["items"], list)
    assert result["items"][0] == "Simple <strong>value</strong>"

    text_objs = [x for x in result["items"] if isinstance(x, dict) and "text" in x]
    assert any(obj["text"] == "Hi {first_name}" for obj in text_objs)

    info_objs = [x for x in result["items"] if isinstance(x, dict) and "info" in x]
    assert len(info_objs) == 1
    assert info_objs[0]["info"] == ["Info1", "Info2"]
