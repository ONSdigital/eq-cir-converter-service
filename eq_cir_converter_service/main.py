"""This module is the entry point of the FastAPI application."""

import fastapi

import eq_cir_converter_service.exception.exception_interceptor as ExceptionInterceptor
from eq_cir_converter_service.exception import exceptions
from eq_cir_converter_service.routers import schema_router

app = fastapi.FastAPI()

app.add_exception_handler(
    exceptions.SchemaProcessingException,
    ExceptionInterceptor.throw_exception_500_schema_processing,
)
app.add_exception_handler(
    exceptions.InvalidCurrentVersionException,
    ExceptionInterceptor.throw_exception_400_invalid_current_version,
)
app.add_exception_handler(
    exceptions.InvalidTargetVersionException,
    ExceptionInterceptor.throw_exception_400_invalid_target_version,
)
app.add_exception_handler(
    exceptions.InputJSONValidationException,
    ExceptionInterceptor.throw_exception_400_empty_input_json,
)

app.include_router(schema_router.router)
