"""Utility functions."""

from fastapi import HTTPException, status
from semver import VersionInfo

from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.exception import exception_messages

logger = logging.getLogger(__name__)


def validate_version(version: str, version_type: str) -> None:
    """Checks if the version matches the regex pattern.

    Parameters:
    - version: The version to validate.
    - version_type: The type of version (current or target).
    """
    try:
        VersionInfo.parse(version)
    except ValueError as exception:
        logger.exception("Invalid %s version: %s", version_type, version)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": exception_messages.exception_400_invalid_version(version_type)},
        ) from exception
