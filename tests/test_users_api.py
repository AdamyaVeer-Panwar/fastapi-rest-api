from fastapi.testclient import TestClient
from main import app
import uuid


def test_create_user():
    unique_email = f"{uuid.uuid4()}@example.com"

    with TestClient(app) as client:
        response = client.post(
            "/users",
            json={
                "name": "Test User",
                "email": unique_email
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == unique_email


def test_get_users():
    with TestClient(app) as client:
        response = client.get("/users")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)