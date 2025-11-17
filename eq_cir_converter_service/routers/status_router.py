from fastapi import APIRouter
from structlog import get_logger

router = APIRouter()
logger = get_logger()

@router.get("/status")
async def health_check() -> dict:
    """Health check endpoint for Cloud Run."""

    logger.info("Health check endpoint.")
    return {"status": "OK"}