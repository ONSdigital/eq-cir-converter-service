"""This module contains the exception responder for the FastAPI application."""

from fastapi.responses import JSONResponse

from eq_cir_converter_service.exception.exception_response_models import ExceptionResponseModel


class ExceptionResponder:
    """The class to respond to exceptions with a JSON response."""

    status_code: int
    response: ExceptionResponseModel

    def __init__(self, status_code: int, response: ExceptionResponseModel) -> None:
        """Initialise the ExceptionResponder."""
        self.status_code = status_code
        self.response = response

    def throw_exception_with_json(self) -> JSONResponse:
        """Throw the exception with a JSON response."""
        return JSONResponse(
            status_code=self.status_code,
            content=self.response.__dict__,
        )
