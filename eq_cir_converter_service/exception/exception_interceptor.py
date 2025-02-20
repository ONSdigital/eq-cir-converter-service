"""This module contains the exception interceptor for the FastAPI application."""

from typing import Any

from fastapi import Request, status

import eq_cir_converter_service.exception.exception_response_models as erm
from eq_cir_converter_service.exception.exception_responder import ExceptionResponder


class ExceptionInterceptor:
    """The class to intercept exceptions and return the appropriate HTTP response."""

    @staticmethod
    def throw_500_schema_processing_exception(request: Request, exc: Exception) -> Any:
        """When an exception is raised and a global error 500 HTTP response is returned."""
        er = ExceptionResponder(status.HTTP_500_INTERNAL_SERVER_ERROR, erm.erm_500_schema_processing_exception)
        return er.throw_er_with_json()

    @staticmethod
    def throw_400_invalid_current_version_exception(request: Request, exc: Exception) -> Any:
        """When a validation fails and a 400 HTTP response is returned."""
        er = ExceptionResponder(status.HTTP_400_BAD_REQUEST, erm.erm_400_invalid_current_version_exception)
        return er.throw_er_with_json()

    @staticmethod
    def throw_400_invalid_target_version_exception(request: Request, exc: Exception) -> Any:
        """When a validation fails and a 400 HTTP response is returned."""
        er = ExceptionResponder(status.HTTP_400_BAD_REQUEST, erm.erm_400_invalid_target_version_exception)
        return er.throw_er_with_json()

    @staticmethod
    def throw_400_empty_input_json_exception(request: Request, exc: Exception) -> Any:
        """When a validation fails and a 400 HTTP response is returned."""
        er = ExceptionResponder(status.HTTP_400_BAD_REQUEST, erm.erm_400_empty_input_json_exception)
        return er.throw_er_with_json()


exception_interceptor = ExceptionInterceptor()
