from fastapi import APIRouter

from src.logging_config import logging

router = APIRouter()

logger = logging.getLogger(__name__)


# The POST endpoint to convert the CIR schema from one version to another
@router.post(
    "/convert/schema",
    response_model=dict,
)
async def post_schema(
    current_version: str,
    target_version: str,
    schema: dict,
) -> dict:
    logger.info("Posting the cir schema...")
    logger.debug(f"Input body: {{{schema}}}")

    # TO DO: Implement the logic to convert the schema from one version to another

    return schema
