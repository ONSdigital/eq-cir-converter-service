"""This module contains the request validators for the EQ CIR Converter Service."""

import re

from fastapi import HTTPException, status

from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.exception import exception_messages

logger = logging.getLogger(__name__)


def validate_version(version: str, version_type: str) -> None:
    """Checks if the version matches the regex pattern.

    Parameters:
    - version: The version to validate.
    - version_type: The type of version (current or target).
    """
    pattern = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$"

    if re.match(pattern, version):
        logger.info(f"The {version_type} version matches the pattern")

    else:
        logger.error(f"Invalid {version_type} version {version}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": exception_messages.exception_400_invalid_version(version_type)},
        )


def validate_input_json(schema: dict) -> None:
    """Validates the input JSON schema to ensure it is not empty.

    Parameters:
    - schema: The input JSON schema.
    """
    if not schema:
        logger.error("Input JSON schema is empty")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": exception_messages.exception_400_empty_input_json},
        )

    logger.info("Input JSON schema is not empty")
