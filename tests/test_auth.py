from app.core.security import hash_password
from app.models.user import User


def test_login_success(client, db):
    user = User(
        username="testcashier",
        password_hash=hash_password("password123"),
        full_name="Test Cashier",
        role="cashier",
        is_active=True,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        json={
            "username": "testcashier",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, db):
    user = User(
        username="testcashier",
        password_hash=hash_password("password123"),
        full_name="Test Cashier",
        role="cashier",
        is_active=True,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        json={
            "username": "testcashier",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


def test_login_unknown_user(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "does-not-exist",
            "password": "password123",
        },
    )

    assert response.status_code == 401
