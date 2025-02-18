"""This module contains the Pydantic models for the exception responses that are returned by the API."""

from pydantic import BaseModel


class ExceptionResponseModel(BaseModel):
    """The Pydantic model for the exception response."""

    status: str
    message: str


erm_500_schema_processing_exception = ExceptionResponseModel(
    status="error", message="Error encountered while processing the schema"
)

erm_400_invalid_current_version_exception = ExceptionResponseModel(
    status="error", message="Invalid current version received"
)

erm_400_invalid_target_version_exception = ExceptionResponseModel(
    status="error", message="Invalid target version received"
)

erm_400_empty_input_json_exception = ExceptionResponseModel(status="error", message="Input JSON schema is empty")
