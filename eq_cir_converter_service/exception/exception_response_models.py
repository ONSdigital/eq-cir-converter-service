"""This module contains the Pydantic models for the exception responses that are returned by the API."""

from pydantic import BaseModel
from eq_cir_converter_service.config.config_helpers import get_current_version_env, get_target_version_env

env_current_version = get_current_version_env()
env_target_version = get_target_version_env()


class ExceptionResponseModel(BaseModel):
    """The Pydantic model for the exception response."""

    status: str
    message: str


erm_500_schema_processing_exception = ExceptionResponseModel(
    status="error", message="Error encountered while processing the schema"
)

erm_400_invalid_current_version_exception = ExceptionResponseModel(
    status="error", message=f"Invalid current version received, expected version is {env_current_version}"
)

erm_400_invalid_target_version_exception = ExceptionResponseModel(
    status="error", message=f"Invalid target version received, expected version is {env_target_version}"
)

erm_400_empty_input_json_exception = ExceptionResponseModel(status="error", message="Input JSON schema is empty")
