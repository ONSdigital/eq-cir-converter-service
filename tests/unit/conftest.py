"""Configuration for unit tests."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

import eq_cir_converter_service.main as app


@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    """General client for hitting endpoints in tests."""
    yield TestClient(app.app)

@pytest.fixture
def placeholder_obj():
    """Fixture to provide a sample placeholder object."""
    yield {"placeholder": "first_name", "value": {"source": "metadata", "identifier": "FIRST_NAME"}}

@pytest.fixture
def sample_json():
    """Provides a sample JSON structure for transform_json testing."""
    yield {
        "description": [
            {
                "text": (
                    "<p>Please note: what constitutes a &#x2018;significant change&#x2019; is dependent on "
                    "your own interpretation in relation to {trad_as}&#x2019;s figures from the previous reporting "
                    "period and the same reporting period last year.</p>"
                    "<p>This information will help us to validate your data and should reduce the need to query any "
                    "figures with you.</p>"
                ),
                "placeholders": [
                    {
                        "placeholder": "trad_as",
                        "transforms": [
                            {
                                "transform": "first_non_empty_item",
                                "arguments": {
                                    "items": [
                                        {"source": "metadata", "identifier": "trad_as"},
                                        {"source": "metadata", "identifier": "ru_name"},
                                    ],
                                },
                            },
                        ],
                    },
                ],
            },
        ],
        "nested": {
            "html": "<b>Bold</b>",
            "list": ["<b>item1</b>", "item2"],
        },
    }
