"""This module converts the schema from the current to the target version."""

from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.exception import exceptions

logger = logging.getLogger(__name__)


class SchemaProcessorService:
    """Service class for processing the schema."""

    @staticmethod
    def convert_schema(current_version: str, target_version: str, schema: dict) -> dict:
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

        if schema == {"simulate_processing_exception": "simulate_processing_exception"}:
            logger.error("Simulating schema processing exception")
            raise exceptions.SchemaProcessingException

        return schema
