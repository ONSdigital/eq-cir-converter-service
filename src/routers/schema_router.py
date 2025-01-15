from fastapi import APIRouter

router = APIRouter()


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
    return schema
