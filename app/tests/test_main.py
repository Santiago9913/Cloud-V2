from sqlmodel import create_engine, Session, SQLModel
from app.main import app
from utils.db_engine import get_session
from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient
from jose import jwt
from env import JWT_SECRET_KEY, ALGORITHM


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"


engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
)


def override_get_session():
    try:
        with Session(engine) as session:
            yield session
    finally:
        session.close()


SQLModel.metadata.create_all(bind=engine)

app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/auth/signup",
        json={
            "name": "Test",
            "email": "test@test.com",
            "password": "test",
        },
    )

    assert response.status_code == 200
    print(response.json())
    data = response.json()

    assert data["name"] == "Test"
    assert data["email"] == "test@test.com"


def test_get_user():
    token = jwt.encode(
        {"email": "test@test.com"},
        key=JWT_SECRET_KEY,
        algorithm=ALGORITHM,
    )
    response = client.get(
        "/users",
        headers={"Authorization": f"Bearer {token}"},
    )
    print(response.json())
    assert response.status_code == 200
