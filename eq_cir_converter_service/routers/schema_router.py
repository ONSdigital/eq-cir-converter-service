"""This module contains the FastAPI router for the schema conversion endpoint."""

from collections.abc import Mapping
from typing import Union

from fastapi import APIRouter, HTTPException

import eq_cir_converter_service.services.schema.schema_processor_service as SchemaProcessorService
from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.exception import exception_messages
from eq_cir_converter_service.services.validators.request_validator import (
    validate_input_json,
    validate_version,
)

router = APIRouter()

logger = logging.getLogger(__name__)

"""The POST endpoint to convert the CIR schema from one version to another."""


@router.post(
    "/schema",
    response_model=dict,
)
async def post_schema(
    current_version: str,
    target_version: str,
    schema: Mapping[str, Union[bool, int, str, list, object]],
) -> dict[str, Union[bool, int, str, list, object]]:
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
    logger.debug("Received schema: %s", schema)

    """Validate the current and target version."""

    validate_version(current_version, "current")
    validate_version(target_version, "target")

    """Validate the input JSON schema."""

    validate_input_json(schema)

    try:
        # TO DO: Implement the logic to convert the schema from one version to another
        # The logic should be implemented in the services package

        return await SchemaProcessorService.convert_schema(current_version, target_version, schema)

    except Exception as exc:

        logger.error("An exception occurred while processing the schema", exc_info=exc)
        raise HTTPException(
            status_code=500, detail={"status": "error", "message": exception_messages.exception_500_schema_processing}
        ) from exc
