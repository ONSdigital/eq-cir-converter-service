"""This module contains the FastAPI router for the Status endpoint.

Provides a simple GET endpoint for Cloud Run to verify that the CIR Converter Service is healthy.
"""

from fastapi import APIRouter
from structlog import get_logger

router = APIRouter()
logger = get_logger()


@router.get("/status")
async def health_check() -> dict:
    """Health check endpoint for Cloud Run.

    Returns:
        dict: A JSON object indicating the service is running.
              Example: {"status": "OK"}
    """
    logger.info("Health check endpoint.")
    return {"status": "OK"}
