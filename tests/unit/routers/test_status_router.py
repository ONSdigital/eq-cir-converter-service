"""This module contains the unit tests for the /status router."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from eq_cir_converter_service.routers.status_router import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_status_endpoint_with_logs(caplog):
    """Test the GET /status endpoint and log output."""

    with caplog.at_level("INFO"):
        response = client.get("/status")

    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
    assert "Health check endpoint." in caplog.text


@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
def test_status_unsupported_method(method):
    """Test that unsupported methods on /status return 405."""
    response = client.request(method, "/status")
    assert response.status_code == 405