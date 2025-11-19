"""This module is the entry point of the FastAPI application."""

import fastapi

from eq_cir_converter_service.config.logging_config import setup_logging
from eq_cir_converter_service.routers import schema_router, status_router

setup_logging()
app = fastapi.FastAPI()

app.include_router(schema_router.router)
app.include_router(status_router.router)
