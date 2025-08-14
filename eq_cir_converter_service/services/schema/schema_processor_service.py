"""This module converts the schema from the current to the target version."""

import copy

from jsonpath_ng.ext import parse

from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.services.schema.extractable_strings import (
    PATHS,
)
from eq_cir_converter_service.types.custom_types import Schema
from eq_cir_converter_service.utils.helper_utils import process_element

logger = logging.getLogger(__name__)


def process_context_dict(context: dict, key: str) -> None:
    """Processes a dictionary context by updating the value at the given key."""
    context[key] = process_element(context[key])


def process_context_list(context: list, index: int) -> None:
    """Processes a list context by updating or expanding the value at the given index."""
    processed = process_element(context[index])
    if isinstance(processed, list):
        context[index : index + 1] = processed
    else:
        context[index] = processed


# --- JSONPath-Based Transformation ---
def transform_json_schema(schema: Schema, paths: list[str]) -> Schema:
    """Transforms the JSON schema based on the provided JSONPath expressions.

    Parameters:
    - schema: The input schema to transform.
    - paths: A sequence of dictionaries containing JSONPath expressions to apply.

    Returns:
    - A new schema with the transformations applied.
    """
    converted_schema = copy.deepcopy(schema)

    for path in paths:
        expr = parse(path)
        for match in expr.find(converted_schema):
            context = match.context.value
            key = match.path.fields[0] if hasattr(match.path, "fields") else None
            index = getattr(match.path, "index", None)

            if isinstance(context, dict) and key:
                process_context_dict(context, key)
            elif isinstance(context, list) and index is not None:
                process_context_list(context, index)

    return converted_schema


# --- Schema Conversion Service ---
def convert_schema(current_version: str, target_version: str, schema: Schema) -> Schema:
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

    logger.debug("Extractable strings for transformation: %s", PATHS)

    if target_version == "10.0.0":
        # If the target version is 10.0.0, we need to transform the schema
        logger.info("Transforming schema for version 10.0.0")
        converted_schema = transform_json_schema(input_schema, PATHS)
    else:
        # For other versions, we can assume no specific transformation is needed
        logger.info("No specific transformation for version %s, using input schema as is", target_version)
        converted_schema = input_schema

    logger.debug("Converted schema: %s", converted_schema)
    logger.info("Schema converted successfully")

    return converted_schema
