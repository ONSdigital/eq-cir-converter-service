"""This module contains the unit tests for the /status router."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from eq_cir_converter_service.routers.status_router import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_status_endpoint():
    """Test the GET /status endpoint."""
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
