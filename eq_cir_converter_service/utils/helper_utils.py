"""Utility functions."""

from fastapi import HTTPException, status
from semver import VersionInfo
from structlog import get_logger

from eq_cir_converter_service.exception import exception_messages

logger = get_logger()


def validate_version(version: str, version_type: str) -> None:
    """Checks if the version matches the regex pattern.

    Parameters:
    - version: The version to validate.
    - version_type: The type of version (current or target).

    Raises:
    - HTTPException: If the version is invalid.
    """
    try:
        VersionInfo.parse(version)
    except ValueError as exception:
        logger.exception("Invalid version", version_type=version_type, version=version)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": exception_messages.exception_400_invalid_version(version_type)},
        ) from exception
