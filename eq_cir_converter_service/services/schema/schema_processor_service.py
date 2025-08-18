"""This module converts the schema from the current to the target version."""

import copy

from jsonpath_ng.ext import parse

from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.services.schema.paths import (
    PATHS,
)
from eq_cir_converter_service.types.custom_types import Schema
from eq_cir_converter_service.utils.helper_utils import process_element

logger = logging.getLogger(__name__)


def process_context_dict(context: dict) -> None:
    """Processes a dictionary context by updating the value at the given key."""
    # Key is always the first element, dict has one key-value pair, hence we can use `next(iter(context))`
    key = next(iter(context))
    context[key] = process_element(context[key])


def process_context_list(context: list, index: int) -> None:
    """Processes a list context by updating or expanding the value at the given index."""
    processed = process_element(context[index])
    if isinstance(processed, list):
        # Replacing a slice of a list (context) with the value of "processed" to accommodate placeholder objects
        context[index : index + 1] = processed
    else:
        context[index] = processed


# --- JSONPath-Based Transformation ---
def convert_to_version_10_0_0(schema: Schema, paths: list[str]) -> Schema:
    """Transforms the schema dictionary based on the provided JSONPath expressions.

    Parameters:
    - schema: The input schema to transform.
    - paths: A list containing JSONPath paths to look for.

    Returns:
    - A new schema with the transformations applied.
    """
    transformed_schema = copy.deepcopy(schema)
    for path in paths:
        jsonpath_expression = parse(path)
        # Extracting and looping through values using JsonPath
        for extracted_value in jsonpath_expression.find(transformed_schema):
            # The result of JsonPath.find provides detailed "context" and "path data", making use of both
            context = extracted_value.context.value
            path_data = extracted_value.path
            # Process the context based on its type (list), index only appears if the context is a list, it increases
            # as we loop through the list
            if (index := getattr(path_data, "index", None)) is not None:
                process_context_list(context, index)
            # Process the context based on its type (dict)
            elif isinstance(context, dict):
                process_context_dict(context)

    return transformed_schema


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

    logger.debug("Extractable strings for conversion to version 10.0.0: %s", PATHS)

    if target_version == "10.0.0":
        # If the target version is 10.0.0, we need to transform the schema
        logger.info("Converting schema to version 10.0.0")
        output_schema = convert_to_version_10_0_0(input_schema, PATHS)
        logger.info("Schema converted successfully")
    else:
        # For other versions, we can assume no specific conversion is needed
        logger.info("No conversions needed for target version %s, using input schema as is", target_version)
        output_schema = input_schema

    logger.debug("Output schema: %s", output_schema)

    return output_schema
