"""This module converts the schema from the current to the target version."""

from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.types.custom_types import ConvertedSchema, InputSchema

logger = logging.getLogger(__name__)


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
    logger.debug("Current version: %s", current_version)
    logger.debug("Target version: %s", target_version)

    if current_version != target_version:
        raise ValueError()

    return dict(schema)
