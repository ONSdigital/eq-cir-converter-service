"""This module contains the query parameter validator service."""

import re

from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.exception import exceptions

logger = logging.getLogger(__name__)


def validate_current_target_version(current_version: str, target_version: str) -> None:
    """Validates the current and target version in the request parameters using the regex pattern x.y.z where x, y, z are numbers.

    Also, validates the current and target version against the environment variables.

    Parameters:
    - current_version: The current version of the schema.
    - target_version: The target version of the schema.
    """
    pattern = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$"

    if re.match(pattern, current_version):
        logger.info("Current version matches the pattern")

    else:
        logger.error("Invalid current version %s", current_version)
        raise exceptions.InvalidCurrentVersionException

    if re.match(pattern, target_version):
        logger.info("Target version matches the pattern")

    else:
        logger.error("Invalid target version %s", target_version)
        raise exceptions.InvalidTargetVersionException


def validate_input_json(schema: dict) -> None:
    """Validates the input JSON schema to ensure it is not empty.

    Parameters:
    - schema: The input JSON schema.
    """
    if not schema:
        logger.error("Input JSON schema is empty")
        raise exceptions.InputJSONValidationException
    logger.info("Input JSON schema is not empty")
