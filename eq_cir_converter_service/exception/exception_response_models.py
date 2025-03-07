"""This module contains the Pydantic models for the exception responses that are returned by the API."""

from pydantic import BaseModel


class ExceptionResponseModel(BaseModel):
    """The Pydantic model for the exception response."""

    status: str
    message: str


exception_500_schema_processing = ExceptionResponseModel(
    status="error", message="Error encountered while processing the schema"
)

exception_400_invalid_current_version = ExceptionResponseModel(
    status="error", message="The current version must be in the format x.y.z where x, y, z are numbers"
)

exception_400_invalid_target_version = ExceptionResponseModel(
    status="error", message="The target version must be in the format x.y.z where x, y, z are numbers"
)

exception_400_empty_input_json = ExceptionResponseModel(status="error", message="Input JSON schema is empty")
