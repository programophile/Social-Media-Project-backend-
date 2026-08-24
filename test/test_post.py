from typing import List
from app import schemas,models
import pytest

def test_get_all_posts(authorized_client,test_posts):
    res=authorized_client.get("/posts/")
    posts_out=[schemas.PostOut(**post) for post in res.json()]
    assert res.status_code==200