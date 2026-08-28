from typing import List
from app import schemas, models
from app.database import get_db
from app.main import app
import pytest
from fastapi.testclient import TestClient


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    posts_out = [schemas.PostOut(**post) for post in res.json()]
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_create_post(authorized_client, test_user):
    payload = {
        "title": "new post title",
        "content": "new post content",
        "published": True,
    }

    res = authorized_client.post("/posts/", json=payload)

    assert res.status_code == 201
    assert res.json()["title"] == payload["title"]
    assert res.json()["content"] == payload["content"]
    assert res.json()["owner_id"] == test_user["id"]


def test_create_post_unauthorized(client):
    payload = {
        "title": "unauthorized post",
        "content": "should fail",
        "published": True,
    }

    res = client.post("/posts/", json=payload)

    assert res.status_code == 401


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 200
    assert res.json()["Post"]["title"] == test_posts[0].title
    assert res.json()["votes"] == 0


def test_update_post(authorized_client, test_posts):
    payload = {
        "title": "updated title",
        "content": "updated content",
        "published": False,
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=payload)

    assert res.status_code == 200
    assert res.json()["title"] == payload["title"]
    assert res.json()["content"] == payload["content"]
    assert res.json()["published"] is False


def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_post_requires_ownership(authorized_client, test_posts, client, session):
    second_user_payload = {"email": "second@example.com", "password": "password123"}
    second_user_res = client.post("/users/", json=second_user_payload)
    second_user = second_user_res.json()

    from app.routers.oauth2 import create_access_token
    token = create_access_token({"user_id": second_user["id"]})

    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    second_client = TestClient(app)
    second_client.headers = {"Authorization": f"Bearer {token}"}

    res = second_client.delete(f"/posts/{test_posts[0].id}")
    app.dependency_overrides.clear()

    assert res.status_code == 403


