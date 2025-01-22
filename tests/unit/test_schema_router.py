from fastapi import status


def test_post_schema_with_valid_json(test_client):
    response = test_client.post(
        "/convert/schema?current_version=1&target_version=2",
        json={"valid_json": "valid_json"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["valid_json"] == "valid_json"
