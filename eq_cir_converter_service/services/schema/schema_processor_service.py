"""This module converts the schema from the current to the target version."""

from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.types.custom_types import ConvertedSchema, InputSchema
from eq_cir_converter_service.utils.text_utils import clean_text, split_paragraphs

logger = logging.getLogger(__name__)


def process_description(
    description: list[dict[str, str | list | object] | str],
) -> list[dict[str, str | list | object] | str]:
    """Processes the description field by cleaning and splitting."""
    logger.debug("Processing description: %s", description)

    processed_description: list[dict[str, str | list | object] | str] = []

    for item in description:
        if isinstance(item, dict) and "text" in item and isinstance(item["text"], str):
            paragraphs = split_paragraphs(item["text"])

            if paragraphs:
                # First part retains placeholders
                first_part = {"text": clean_text(paragraphs[0]), "placeholders": item.get("placeholders", [])}
                processed_description.append(first_part)

                # Remaining parts added as plain strings
                processed_description.extend(paragraphs[1:])
        elif isinstance(item, str):
            # If the item is a string, clean it and add to the new description
            # This handles cases where the description is a list of strings
            processed_description.append(clean_text(item))
        else:
            # If the item is neither a dict nor a string, we can skip it or handle it as needed
            logger.warning("Unexpected item type in description: %s", type(item))
            continue

    logger.debug("Processed description: %s", processed_description)
    return processed_description


def transform_json(json_data: dict | list | str) -> dict | list | str:
    """Recursively transforms the JSON structure."""
    logger.debug("Transforming JSON data: %s", json_data)

    # Check if the JSON data is a dictionary or a list
    if isinstance(json_data, dict):
        logger.debug("Processing dictionary")

        # Iterate through the dictionary items
        for key, value in json_data.items():
            if isinstance(value, str):
                json_data[key] = clean_text(value)
                logger.debug("Cleaned string value for key '%s': %s", key, json_data[key])
            elif key == "description" and isinstance(value, list):
                json_data[key] = process_description(value)
                logger.debug("Processed description: %s", json_data[key])
            else:
                json_data[key] = transform_json(value)
                logger.debug("Transformed value for key '%s': %s", key, json_data[key])

    # If the JSON data is a list, process each item in the list
    elif isinstance(json_data, list):
        json_data = [transform_json(item) for item in json_data]
        logger.debug("Transformed list: %s", json_data)

    elif isinstance(json_data, str):
        logger.debug("Processing other data type: %s", json_data)
        json_data = clean_text(json_data)
        logger.debug("Transformed JSON data: %s", json_data)

    return json_data


def convert_schema(current_version: str, target_version: str, schema: InputSchema) -> ConvertedSchema:
    """Converts the schema from the current to the target version.

    Parameters:
    - current_version: The current version of the schema.
    - target_version: The target version of the schema.
    - schema: The schema to convert.

    Returns:
    - dict: The converted schema.
    """
    logger.info("Converting the schema...")

    logger.debug("Current version: %s", current_version)
    logger.debug("Target version: %s", target_version)

    input_schema = dict(schema)

    logger.debug("Input schema: %s", input_schema)

    if target_version == "10.0.0":
        # If the target version is 10.0.0, we need to transform the schema
        logger.info("Transforming schema for version 10.0.0")
        converted_schema = transform_json(input_schema)
    else:
        # For other versions, we can assume no specific transformation is needed
        logger.info("No specific transformation for version %s, using input schema as is", target_version)
        converted_schema = input_schema

    logger.debug("Converted schema: %s", converted_schema)
    logger.info("Schema converted successfully")

    return converted_schema
