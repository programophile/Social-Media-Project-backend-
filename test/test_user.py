from app import schemas
from .database import client, session

# Test root endpoint
def test_root(client):
    response = client.get("/")

    assert response.status_code == 200


# Test creating a user
def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "email": "sad@gmail.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201
    assert response.json()["email"] == "sad@gmail.com"