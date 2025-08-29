"""This module converts the schema from the current to the target version."""

from copy import deepcopy

from jsonpath_ng.ext import parse
from structlog import get_logger

from eq_cir_converter_service.converters.v10 import (
    process_context_dict,
    process_context_list,
)
from eq_cir_converter_service.services.schema.paths import (
    PATHS,
)
from eq_cir_converter_service.types.custom_types import Schema

logger = get_logger()


# --- JSONPath-Based Transformation ---
def convert_to_v10(schema: Schema, paths: list[str]) -> Schema:
    """Transforms the schema dictionary based on the provided JSONPath expressions.

    Parameters:
    - schema: The input schema to transform.
    - paths: A list containing JSONPath paths to look for.

    Returns:
    - A new schema with the transformations applied.
    """
    transformed_schema = deepcopy(schema)
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
    logger.debug("Converting the schema...")

    logger.debug("Current version:", current_version=current_version)
    logger.debug("Target version:", target_version=current_version)

    input_schema = dict(schema)

    logger.debug("Input schema:", input_schema=input_schema)

    logger.debug("Extractable strings for conversion to version 10.0.0:", paths=PATHS)

    # If the target version is 10 transform the schema
    if target_version == "10.0.0":
        logger.debug("Converting schema to version 10.0.0...")
        output_schema = convert_to_v10(input_schema, PATHS)
        logger.info("Schema converted successfully")
    # For other versions do not apply conversion
    else:
        logger.info("No conversions needed for target version, using input schema as is", target_version=target_version)
        output_schema = input_schema

    logger.debug("Output schema:", output_schema=output_schema)

    return output_schema
