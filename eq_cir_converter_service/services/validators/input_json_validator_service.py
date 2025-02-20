"""This module contains the service class for validating the input JSON."""

from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.exception import exceptions

logger = logging.getLogger(__name__)


class InputJSONValidatorService:
    """Service class for validating the input JSON."""

    @staticmethod
    def validate_input_json(schema: dict) -> None:
        """Validates the input JSON schema to ensure it is not empty.

        Parameters:
        - schema: The input JSON schema.
        """
        if not schema:
            logger.error("Input JSON schema is empty")
            raise exceptions.InputJSONValidationException
        logger.info("Input JSON schema is not empty")
