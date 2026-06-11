from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_user():

    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "test@example.com"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"