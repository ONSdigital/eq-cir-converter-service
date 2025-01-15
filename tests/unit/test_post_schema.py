from unittest import TestCase

import pytest
from fastapi import status


class PostSchemaTest(TestCase):
    @pytest.fixture(autouse=True)
    def prepare_fixture(self, test_client):
        self.test_client = test_client

    def test_post_schema_with_valid_json(self):
        response = self.test_client.post(
            "/convert/schema?current_version=1&target_version=2",
            json={"valid_json": "valid_json"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["valid_json"] == "valid_json"
