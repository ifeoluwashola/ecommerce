import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal, engine
from app.models import Base

# Constants
BASE_URL = "http://test"

# Setup and teardown for testing database
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield SessionLocal()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.mark.asyncio
def test_register_user(client):
    response = client.post("/api/users/register", json={
        "email": "testuser+3@example.com",
        "password": "password0123",
        "first_name": "Test3",
        "last_name": "User3",
        "phone_number": "01235679890"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "testuser+3@example.com"

@pytest.mark.asyncio
def test_login_user(client):
    # Assuming user is already registered
    response = client.post("/api/users/login", json={
        "email": "testuser+3@example.com",
        "password": "password0123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
def test_get_profile(client):
    login_response = client.post("/api/users/login", json={
        "email": "user@example.com",
        "password": "newpassword"
    })
    token = login_response.json()["access_token"]
    response = client.get("/api/users/profile", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"

@pytest.mark.asyncio
def test_avatar_upload(client):
    login_response = client.post("/api/users/login", json={
        "email": "user@example.com",
        "password": "newpassword"
    })
    token = login_response.json()["access_token"]
    files = {"file": ("avatar.jpg", b"fake-image-content", "image/jpeg")}
    response = client.post("/api/users/avatar", headers={"Authorization": f"Bearer {token}"}, files=files)
    assert response.status_code == 200
    assert "avatar_url" in response.json()

@pytest.mark.asyncio
def test_password_reset(client):
    # Request password reset
    response = client.post("/api/users/password-reset/request", json={
        "email": "user@example.com"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Password reset email sent."

    # Confirm password reset (use a valid token here)
    reset_token = "replace_with_valid_token"  # Mock this in tests
    new_password = "newpassword123"
    response = client.post("/api/users/password-reset/confirm", json={
        "token": reset_token,
        "new_password": new_password
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully."
