"""This module is the entry point of the FastAPI application."""

import fastapi

from eq_cir_converter_service.routers import schema_router

app = fastapi.FastAPI()

app.include_router(schema_router.router)
