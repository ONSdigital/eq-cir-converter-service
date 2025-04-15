"""This module converts the schema from the current to the target version."""

import re
from typing import Any

from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.types.custom_types import ConvertedSchema, InputSchema

logger = logging.getLogger(__name__)


def replace_b_with_strong(text: str) -> str:
    """Replaces <b> and </b> tags with <strong> and </strong>."""
    
    logger.debug("Replacing <b> with <strong> in text: %s", text)
    
    # Replace <b> with <strong> and </b> with </strong>
    text = re.sub(r"<\s*b\s*>", "<strong>", text, flags=re.IGNORECASE)
    text = re.sub(r"<\s*/\s*b\s*>", "</strong>", text, flags=re.IGNORECASE)
    return text


def split_paragraphs(text: str) -> list[str]:
    """Splits the text content by <p>...</p> and returns cleaned parts."""

    logger.debug("Splitting paragraphs from text: %s", text)

    # Use regex to find all <p>...</p> sections
    parts = re.findall(r"<p>(.*?)</p>", text, flags=re.DOTALL)
    logger.debug("Split paragraphs: %s", parts)
    return [part.strip() for part in parts if part.strip()]


def clean_text(text: str) -> str:
    """Removes <p> tags and splits text based on occurrences of {string}."""
    
    logger.debug("Cleaning text: %s", text)

    text = re.sub(r"</?p>", "", text)  # Remove <p> tags
    text = replace_b_with_strong(text)  # Replace <b> with <strong>
    logger.debug("Cleaned text: %s", text)
    return text.strip()


def process_description(description: list[dict[str, Any] | str]) -> list[dict[str, Any] | str]:
    """Processes the description field by cleaning and splitting."""

    logger.debug("Processing description: %s", description)

    new_description: list[dict[str, Any] | str] = []

    for item in description:
        if isinstance(item, dict) and "text" in item:
            paragraphs = split_paragraphs(item["text"])

            if paragraphs:
                # First part retains placeholders
                first_part = {"text": paragraphs[0], "placeholders": item.get("placeholders", [])}
                new_description.append(first_part)

                # Remaining parts added as plain strings
                new_description.extend(paragraphs[1:])
        elif isinstance(item, str):
            # If the item is a string, clean it and add to the new description
            # This handles cases where the description is a list of strings
            new_description.append(clean_text(item))

    return new_description


def transform_json(json_data: dict) -> dict:
    """Recursively transforms the JSON structure."""

    logger.debug("Transforming JSON data: %s", json_data)

    # Check if the JSON data is a dictionary or a list
    if isinstance(json_data, dict):
        logger.debug("Processing dictionary")

        # Iterate through the dictionary items
        for key, value in json_data.items():
            if isinstance(value, str):
                json_data[key] = clean_text(value)
            elif key == "description" and isinstance(value, list):
                logger.debug("Processing description field")
                json_data[key] = process_description(value)
                logger.debug("Processed description: %s", json_data[key])
            else:
                json_data[key] = transform_json(value)

    # If the JSON data is a list, process each item in the list
    elif isinstance(json_data, list):
        json_data = [transform_json(item) for item in json_data]

    return json_data


async def convert_schema(current_version: str, target_version: str, schema: InputSchema) -> ConvertedSchema:
    """Converts the schema from the current to the target version.

    Parameters:
    - current_version: The current version of the schema.
    - target_version: The target version of the schema.
    - schema: The schema to convert.

    Returns:
    - dict: The converted schema.
    """
    logger.info("Converting the schema...")

    # TO DO: Implement the logic to convert the schema from one version to another

    input_schema = {}

    for key, value in schema.items():
        input_schema[key] = value

    logger.debug("Input schema: %s", input_schema)

    # Transform JSON
    converted_schema = transform_json(input_schema)

    logger.debug("Converted schema: %s", converted_schema)
    logger.info("Schema converted successfully")

    return converted_schema
