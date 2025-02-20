"""This module is the entry point of the FastAPI application."""

import fastapi

from eq_cir_converter_service.exception import exceptions
from eq_cir_converter_service.exception.exception_interceptor import ExceptionInterceptor
from eq_cir_converter_service.routers import schema_router

app = fastapi.FastAPI()

app.add_exception_handler(
    exceptions.SchemaProcessingException,
    ExceptionInterceptor.throw_500_schema_processing_exception,
)
app.add_exception_handler(
    exceptions.InvalidCurrentVersionException,
    ExceptionInterceptor.throw_400_invalid_current_version_exception,
)
app.add_exception_handler(
    exceptions.InvalidTargetVersionException,
    ExceptionInterceptor.throw_400_invalid_target_version_exception,
)
app.add_exception_handler(
    exceptions.InputJSONValidationException,
    ExceptionInterceptor.throw_400_empty_input_json_exception,
)

app.include_router(schema_router.router)
