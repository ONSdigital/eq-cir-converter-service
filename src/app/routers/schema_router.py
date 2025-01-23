"""This module contains the FastAPI router for the schema conversion endpoint."""

from config.logging_config import logging
from fastapi import APIRouter

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
    """Convert the CIR schema from one version to another."""
    logger.info("Posting the cir schema...")

    logger.debug("Received current version %s and target version %s", current_version, target_version)
    logger.debug("Input body: %s", schema)

    # TO DO: Implement the logic to convert the schema from one version to another

    return schema
