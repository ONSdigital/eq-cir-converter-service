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

def split_paragraphs(text):
    """Splits the text content by <p>...</p> and returns cleaned parts."""
    parts = re.findall(r'<p>(.*?)</p>', text, flags=re.DOTALL)
    logger.debug("Split paragraphs: %s", parts)
    return [part.strip() for part in parts if part.strip()]

def clean_text(text):
    """Removes <p> tags and splits text based on occurrences of {string}."""
    text = re.sub(r'</?p>', '', text)  # Remove <p> tags
    text = replace_b_with_strong(text)  # Replace <b> with <strong>
    logger.debug("Cleaned text: %s", text)
    return text.strip()

def process_description(description):
    """Processes the description field by cleaning and splitting."""
    new_description = []
    
    for item in description:
        if isinstance(item, dict) and 'text' in item:
            # cleaned_text = clean_text(item['text'])
            # text_parts = re.split(r'(?<=})', cleaned_text)  # Split at {string} occurrences
            
            # # First part retains placeholders
            # if text_parts:
            #     first_part = {"text": text_parts[0].strip(), "placeholders": item.get("placeholders", [])}
            #     new_description.append(first_part)
                
            #     # Remaining parts are added as separate entries
            #     new_description.extend([part.strip() for part in text_parts[1:] if part.strip()])
            paragraphs = split_paragraphs(item['text'])

            if paragraphs:
                # First part retains placeholders
                first_part = {"text": paragraphs[0], "placeholders": item.get("placeholders", [])}
                new_description.append(first_part)

                # Remaining parts added as plain strings
                new_description.extend(paragraphs[1:])            
        else:
            new_description.append(clean_text(item))
    
    return new_description

def transform_json(json_data):
    """Recursively transforms the JSON structure."""
    if isinstance(json_data, dict):
        logger.debug("Processing dictionary")
        for key, value in json_data.items():
            if isinstance(value, str):
                json_data[key] = clean_text(value)
            elif key == "description" and isinstance(value, list):
                logger.debug("Processing description field")
                json_data[key] = process_description(value)
                logger.debug("Processed description: %s", json_data[key])
            else:
                json_data[key] = transform_json(value)
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

    # Transform JSON
    converted_schema = clean_text(input_schema)
    logger.info("Schema converted successfully")

    return converted_schema
