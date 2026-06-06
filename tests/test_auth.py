from datetime import datetime
from typing import Any

from fastapi.testclient import TestClient

from app.api.dependencies import get_db
from app.core.security import hash_password
from app.main import app
from app.models.user import User


class FakeSession:
    def __init__(self, user: User | None) -> None:
        self.user = user

    def scalar(self, statement: Any) -> User | None:
        return self.user

    def commit(self) -> None:
        pass

    def refresh(self, instance: User) -> None:
        pass

    def close(self) -> None:
        pass


def build_user() -> User:
    return User(
        id=1,
        name="Test User",
        username="testuser",
        email="test@example.com",
        password_hash=hash_password("Password@123"),
        role="user",
        is_active=True,
        created_at=datetime(2026, 1, 1),
        updated_at=datetime(2026, 1, 1),
    )


def test_login_and_get_current_user() -> None:
    user = build_user()

    def override_get_db():
        yield FakeSession(user)

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    try:
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "Password@123"},
        )

        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        me_response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert me_response.status_code == 200
        assert me_response.json()["email"] == "test@example.com"
    finally:
        app.dependency_overrides.clear()


def test_login_rejects_wrong_password() -> None:
    user = build_user()

    def override_get_db():
        yield FakeSession(user)

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    try:
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "WrongPassword"},
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid email, username, or password"
    finally:
        app.dependency_overrides.clear()


def test_me_requires_access_token() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
