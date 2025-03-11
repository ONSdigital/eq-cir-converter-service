"""This module contains the exception interceptor for the FastAPI application."""

from fastapi import Request, status
from fastapi.responses import JSONResponse

from eq_cir_converter_service.exception.exception_responder import ExceptionResponder
from eq_cir_converter_service.exception.exception_response_models import (
    exception_400_empty_input_json,
    exception_400_invalid_current_version,
    exception_400_invalid_target_version,
    exception_500_schema_processing,
)

def throw_exception_500_schema_processing(request: Request, exc: Exception) -> JSONResponse:
    """When an exception is raised and a global error 500 HTTP response is returned."""
    responder = ExceptionResponder(status.HTTP_500_INTERNAL_SERVER_ERROR, exception_500_schema_processing)
    return responder.throw_exception_with_json()

def throw_exception_400_invalid_current_version(request: Request, exc: Exception) -> JSONResponse:
    """When a validation fails and a 400 HTTP response is returned."""
    responder = ExceptionResponder(status.HTTP_400_BAD_REQUEST, exception_400_invalid_current_version)
    return responder.throw_exception_with_json()

def throw_exception_400_invalid_target_version(request: Request, exc: Exception) -> JSONResponse:
    """When a validation fails and a 400 HTTP response is returned."""
    responder = ExceptionResponder(status.HTTP_400_BAD_REQUEST, exception_400_invalid_target_version)
    return responder.throw_exception_with_json()

def throw_exception_400_empty_input_json(request: Request, exc: Exception) -> JSONResponse:
    """When a validation fails and a 400 HTTP response is returned."""
    responder = ExceptionResponder(status.HTTP_400_BAD_REQUEST, exception_400_empty_input_json)
    return responder.throw_exception_with_json()
