"""This module contains the FastAPI router for the schema conversion endpoint."""

from fastapi import APIRouter, HTTPException

from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.exception import exception_messages
from eq_cir_converter_service.services.schema.schema_processor_service import (
    SchemaProcessorService,
)
from eq_cir_converter_service.services.validators.request_validator import (
    validate_current_target_version,
    validate_input_json,
)

router = APIRouter()

logger = logging.getLogger(__name__)

"""The POST endpoint to convert the CIR schema from one version to another."""


@router.post(
    "/schema",
    response_model=dict,
)
async def convert_schema(
    current_version: str,
    target_version: str,
    schema: dict,
) -> dict:
    """Convert the CIR schema from one version to another.

    Request query parameters:
    - current_version: The current version of the schema.
    - target_version: The target version of the schema.

    Request body:
    - schema: The schema to convert.

    Returns:
    - dict: The converted schema.
    """
    logger.info("Posting the cir schema...")

    logger.debug("Received current version %s and target version %s", current_version, target_version)
    logger.debug("Input body: %s", schema)

    """Validate the query parameters and input JSON."""

    validate_current_target_version(current_version, target_version)
    validate_input_json(schema)

    try:
        # TO DO: Implement the logic to convert the schema from one version to another
        # The logic should be implemented in the services package

        converted_schema = SchemaProcessorService.convert_schema(current_version, target_version, schema)

        return converted_schema

    except Exception as exc:

        logger.error("An exception occurred while processing the schema", exc_info=exc)
        raise HTTPException(
            status_code=500, detail={"status": "error", "message": exception_messages.exception_500_schema_processing}
        ) from exc
