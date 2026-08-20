import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.config import settings
from app.database import get_db, Base


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