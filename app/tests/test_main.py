from sqlmodel import create_engine, Session, SQLModel
from app.main import app
from utils.db_engine import get_session
from fastapi.testclient import TestClient


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


def test_signin():
    response = client.post(
        "/auth/signup",
        json={
            "name": "Test",
            "email": "test@test.com",
            "password": "test",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Test"
    assert data["email"] == "test@test.com"


def test_signin():
    response = client.post(
        "/auth/signin",
        json={"email": "test@test.com", "password": "test"},
    )
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert "user" in data
    assert data["user"]["email"] == "test@test.com"
    assert data["user"]["name"] == "Test"
    assert "id" in data["user"]
