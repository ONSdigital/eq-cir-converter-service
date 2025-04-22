"""This module contains the FastAPI router for the schema conversion endpoint."""

from fastapi import APIRouter, HTTPException

import eq_cir_converter_service.services.schema.schema_processor_service as schema_processor_service
from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.exception import exception_messages
from eq_cir_converter_service.services.validators.request_validator import (
    validate_input_json,
    validate_version,
)
from eq_cir_converter_service.types.custom_types import ConvertedSchema, InputSchema

router = APIRouter()

logger = logging.getLogger(__name__)

"""The POST endpoint to convert the CIR schema from one version to another."""


@router.post(
    "/schema",
    response_model=ConvertedSchema,
)
async def post_schema(
    current_version: str,
    target_version: str,
    schema: InputSchema,
) -> ConvertedSchema:
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
    logger.info("Posting the cir schema...")

    logger.debug("Received current version %s and target version %s", current_version, target_version)
    logger.debug("Received schema: %s", schema)

    logger.info("Validating the current and target version...")
    validate_version(current_version, "current")
    validate_version(target_version, "target")

    logger.info("Validating the input JSON schema...")
    validate_input_json(schema)

    try:
        # TO DO: Implement the logic to convert the schema from one version to another
        # The logic should be implemented in the services package.

        return await schema_processor_service.convert_schema(current_version, target_version, schema)

    except ValueError as exc:
        logger.exception("An exception occurred while comparing versions", exc_info=exc)
        raise HTTPException(
            status_code=500,
            detail={"status": "info", "message": exception_messages.EXCEPTION_500_MATCHING_SCHEMA_VERSIONS},
        ) from exc
    except HTTPException as exc:
        logger.exception("An exception occurred while processing the schema", exc_info=exc)
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": exception_messages.EXCEPTION_500_SCHEMA_PROCESSING},
        ) from exc
