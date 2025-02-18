"""This module contains the FastAPI router for the schema conversion endpoint."""

from fastapi import APIRouter

import eq_cir_converter_service.exception.exception_response_models as erm
from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.exception import exceptions
from eq_cir_converter_service.exception.exception_response_models import ExceptionResponseModel
from eq_cir_converter_service.services.schema.schema_processor_service import (
    SchemaProcessorService,
)
from eq_cir_converter_service.services.validators.input_json_validator_service import (
    InputJSONValidatorService,
)
from eq_cir_converter_service.services.validators.query_parameter_validator_service import (
    QueryParameterValidatorService,
)

router = APIRouter()

logger = logging.getLogger(__name__)

"""The POST endpoint to convert the CIR schema from one version to another."""


@router.post(
    "/schema",
    response_model=dict,
    responses={
        400: {
            "model": ExceptionResponseModel,
            "content": {"application/json": {"example": erm.erm_400_invalid_current_version_exception}},
        },
        500: {
            "model": ExceptionResponseModel,
            "content": {"application/json": {"example": erm.erm_500_schema_processing_exception}},
        },
    },
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

    QueryParameterValidatorService.validate_current_target_version(current_version, target_version)
    InputJSONValidatorService.validate_input_json(schema)

    try:
        # TO DO: Implement the logic to convert the schema from one version to another
        # The logic should be implemented in the services package
        SchemaProcessorService.convert_schema(current_version, target_version, schema)
        pass

    except Exception as e:
        logger.error("Error encountered while processing the schema")
        raise exceptions.SchemaProcessingException from e

    return schema
