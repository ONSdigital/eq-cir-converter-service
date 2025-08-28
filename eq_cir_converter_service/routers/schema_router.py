"""This module contains the FastAPI router for the schema conversion endpoint."""

from fastapi import APIRouter, HTTPException, status

from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.exception import exception_messages
from eq_cir_converter_service.services.schema import schema_processor_service
from eq_cir_converter_service.services.validators.request_validator import (
    validate_input_json,
    validate_version,
)
from eq_cir_converter_service.types.custom_types import Schema

router = APIRouter()

logger = logging.getLogger(__name__)

"""The POST endpoint to convert the CIR schema from one version to another."""


@router.post(
    "/schema",
    response_model=Schema,
)
async def post_schema(
    current_version: str,
    target_version: str,
    schema: Schema,
) -> Schema:
    """Convert the CIR schema from one version to another.

    Request query parameters:
    - current_version: The current version of the schema.
    - target_version: The target version of the schema.

    Request body:
    - schema: The schema to convert.

    Steps:
    - Validate the current and target version.
    - Validate the input JSON schema.

    Returns:
    - dict: The converted schema.
    """
    logger.debug("Posting the cir schema...")

    logger.debug("Received current version %s and target version %s", current_version, target_version)
    logger.debug("Received schema: %s", schema)

    logger.debug("Validating the current and target version...")
    validate_version(current_version, "current")
    validate_version(target_version, "target")

    if current_version == target_version:
        logger.debug("The current and target schema versions are the same")
        # Ideally, the caller must not send to the converter service with the same versions.
        # Hence it is the best approach to give an error response.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": exception_messages.EXCEPTION_400_MATCHING_SCHEMA_VERSIONS},
        )

    logger.info("Validating the input JSON schema...")
    validate_input_json(schema)

    try:
        logger.debug(
            "Converting the schema from current version %s to target version %s",
            current_version,
            target_version,
        )
        logger.debug("Converting schema: %s", schema)
        # Call the schema processor service to convert the schema
        return schema_processor_service.convert_schema(current_version, target_version, schema)

    except HTTPException as exc:
        logger.exception("An exception occurred while processing the schema", exc_info=exc)
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": exception_messages.EXCEPTION_500_SCHEMA_PROCESSING},
        ) from exc
