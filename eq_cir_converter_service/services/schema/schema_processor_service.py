"""This module converts the schema from the current to the target version."""

from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.types.custom_types import ConvertedSchema, InputSchema

logger = logging.getLogger(__name__)

import re

def replace_b_with_strong(text):
    """Replaces <b> and </b> tags with <strong> and </strong>."""
    text = re.sub(r'<\s*b\s*>', '<strong>', text, flags=re.IGNORECASE)
    text = re.sub(r'<\s*/\s*b\s*>', '</strong>', text, flags=re.IGNORECASE)
    return text

def clean_text(text):
    """Removes <p> tags and splits text based on occurrences of {string}."""
    text = re.sub(r'</?p>', '', text)  # Remove <p> tags
    text = replace_b_with_strong(text)  # Replace <b> with <strong>
    logger.debug("Cleaned text: %s", text)
    return text.strip()

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

    # Transform JSON
    converted_schema = clean_text(input_schema)
    logger.info("Schema converted successfully")

    return converted_schema
