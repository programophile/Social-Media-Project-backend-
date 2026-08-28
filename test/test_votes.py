from app import schemas


def test_vote_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})

    assert res.status_code == 201
    assert res.json()["message"] == "successfully added vote"


def test_vote_post_twice(authorized_client, test_posts):
    authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})

    assert res.status_code == 409
    assert "already voted" in res.json()["detail"]


def test_remove_vote(authorized_client, test_posts):
    authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": -1})

    assert res.status_code == 201
    assert res.json()["message"] == "successfully deleted vote"


def test_vote_for_missing_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 99999, "dir": 1})

    assert res.status_code == 404


def test_vote_requires_authentication(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})

    assert res.status_code == 401
