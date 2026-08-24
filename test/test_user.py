from app import schemas
# from .database import client, session
import pytest
import jwt
from app.config import settings 




# Test root endpoint
# def test_root(client):
#     response = client.get("/")

#     assert response.status_code == 200


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
def test_login_user(client, test_user):
    response=client.post("/login",data={
            "username": test_user['email'],
            "password": test_user['password']
        })
    # print(response.json())
    login_res=schemas.Token(**response.json())
    payload=jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id=payload.get("user_id")
    assert id==test_user['id']
    assert login_res.token_type=="bearer"
    assert response.status_code==200
@pytest.mark.parametrize("email,password,status_code",[
    ("wrongramil@gmail.com","password123",403),
    ("sad@gmail.com","lkdjlkj",403),
    (None,"password123",422),
    ("sad@gmail.com",None,422)

])

def test_incorrect_login(client, test_user,email,password,status_code):
    res= client.post("/login", data={
        "username": email,
        "password": password
    })
    assert res.status_code==status_code
    