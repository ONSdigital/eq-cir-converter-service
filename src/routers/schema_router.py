from fastapi import APIRouter, Body, Depends

router = APIRouter()

@router.post(
    "/convert/schema",
    response_model = dict,
    #     responses={
    #     400: {
    #         "model": ExceptionResponseModel,
    #         "content": {
    #             "application/json": {"example": erm.erm_400_validation_exception}
    #         },
    #     },
    #     500: {
    #         "model": ExceptionResponseModel,
    #         "content": {"application/json": {"example": erm.erm_500_global_exception}},
    #     },
    # },
)
async def post_schema(
    current_version: str,
    target_version: str,
    schema: dict = Body(...),
) -> dict:
    return schema