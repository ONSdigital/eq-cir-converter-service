"""This module converts the schema from the current to the target version."""

from structlog import get_logger

from eq_cir_converter_service.converters.v10 import convert_to_v10
from eq_cir_converter_service.services.schema.paths import (
    PATHS,
)
from eq_cir_converter_service.types.custom_types import Schema

logger = get_logger()


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
