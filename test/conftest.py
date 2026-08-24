import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.routers.oauth2 import create_access_token
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app import models

# Test database URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://"
    f"{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}_test"
)


# Create engine for test database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Database session fixture
@pytest.fixture()
def session():
    # Start each test with a clean database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


# FastAPI test client fixture
@pytest.fixture()
def client(session):

    def override_get_db():
        yield session

    # Replace the application's database dependency
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    # Remove the override after the test
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(session,client):
    user_data = {"email": "sad@gmail.com","password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    yield new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})
@pytest.fixture
def authorized_client(token,client):
    client.headers={
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user,session):
    posts_data = [
        {"title": "first title", "content": "first content", "owner_id": test_user['id']},
        {"title": "second title", "content": "second content", "owner_id": test_user['id']},
        {"title": "third title", "content": "third content", "owner_id": test_user['id']}
    ]
    session.add_all([models.Post([models.Post(title=post["title"], content=post["content"], owner_id=post["owner_id"]) for post in posts_data])])
    session.commit()
    post=session.query(models.Post).all()
    return post

    # def create_post_model(post):
    #     return models.Post(**post)

    # post_map = map(create_post_model, posts_data)
    # posts = list(post_map)

    # session.add_all(posts)
    # session.commit()

    # yield session.query(models.Post).all()