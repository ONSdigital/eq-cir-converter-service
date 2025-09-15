"""This module converts the schema from the current to the target version."""

from structlog import get_logger

from eq_cir_converter_service.converters.v10 import convert_to_v10
from eq_cir_converter_service.services.schema.paths import (
    PATHS,
)
from eq_cir_converter_service.types.custom_types import Schema

logger = get_logger()


def process_schema(*, current_version: str, target_version: str, input_schema: Schema) -> Schema:
    """Processes the schema and converts from the current to the target version if required.

    Parameters:
    - current_version: The current version of the schema.
    - target_version: The target version of the schema.
    - input_schema: The schema to process.

    Returns:
    - dict: The processed schema.
    """
    logger.debug("Processing the schema...")

    logger.debug("Current version:", current_version=current_version)
    logger.debug("Target version:", target_version=target_version)

    logger.debug("Input schema:", input_schema=input_schema)

    if target_version == "10.0.0":
        logger.debug("Converting schema to version 10.0.0...")
        logger.debug("Extractable strings for conversion to version 10.0.0:", paths=PATHS)

        output_schema = convert_to_v10(input_schema, PATHS)

        logger.info("Schema converted successfully")

        return output_schema

    logger.info("No conversions needed for target version, using input schema as is", target_version=target_version)

    logger.debug("Output schema:", output_schema=input_schema)

    return input_schema
