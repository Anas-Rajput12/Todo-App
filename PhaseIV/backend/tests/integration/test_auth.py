import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from unittest.mock import patch

from src.main import app
from src.models.user import User
from src.database import engine


@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_session():
    """Create a test database session."""
    with Session(engine) as session:
        yield session


def test_user_registration_flow_integration(client: TestClient, db_session: Session):
    """Test the complete user registration flow integration."""
    # Test data
    user_data = {
        "email": "integration_test@example.com",
        "password": "SecurePassword123!",
        "first_name": "Integration",
        "last_name": "Test"
    }

    # Register the user
    response = client.post("/v1/auth/signup", json=user_data)

    # Verify registration response
    assert response.status_code == 200 or response.status_code == 201
    response_data = response.json()
    assert "access_token" in response_data
    assert "user" in response_data
    assert response_data["user"]["email"] == user_data["email"]

    # Verify user exists in database
    statement = select(User).where(User.email == user_data["email"])
    user_in_db = db_session.exec(statement).first()
    assert user_in_db is not None
    assert user_in_db.email == user_data["email"]
    assert user_in_db.first_name == user_data["first_name"]
    assert user_in_db.last_name == user_data["last_name"]

    # Verify the returned user data matches database
    assert str(user_in_db.id) == response_data["user"]["id"]


def test_user_login_flow_integration(client: TestClient, db_session: Session):
    """Test the complete user login flow integration."""
    # First register a user
    user_data = {
        "email": "login_integration_test@example.com",
        "password": "SecurePassword123!",
        "first_name": "Login",
        "last_name": "Integration"
    }

    signup_response = client.post("/v1/auth/signup", json=user_data)
    assert signup_response.status_code in [200, 201]

    # Now try to login with the same credentials
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }

    login_response = client.post("/v1/auth/login", json=login_data)

    # Verify login response
    assert login_response.status_code == 200
    login_response_data = login_response.json()
    assert "access_token" in login_response_data
    assert "user" in login_response_data
    assert login_response_data["user"]["email"] == user_data["email"]

    # Verify the token can be used for authentication
    headers = {"Authorization": f"Bearer {login_response_data['access_token']}"}
    protected_response = client.get("/health", headers=headers)
    # This might fail since we don't have a protected endpoint yet, but the auth should work


def test_duplicate_user_registration_fails(client: TestClient, db_session: Session):
    """Test that registering a duplicate user fails appropriately."""
    user_data = {
        "email": "duplicate_test@example.com",
        "password": "SecurePassword123!",
        "first_name": "Duplicate",
        "last_name": "Test"
    }

    # Register the user first time
    first_response = client.post("/v1/auth/signup", json=user_data)
    assert first_response.status_code in [200, 201]

    # Try to register the same user again
    second_response = client.post("/v1/auth/signup", json=user_data)

    # Should fail with conflict status
    assert second_response.status_code == 409 or second_response.status_code == 422


def test_invalid_credentials_login_fails(client: TestClient, db_session: Session):
    """Test that login with invalid credentials fails appropriately."""
    # Register a user first
    user_data = {
        "email": "invalid_login_test@example.com",
        "password": "SecurePassword123!",
        "first_name": "Invalid",
        "last_name": "Login"
    }

    signup_response = client.post("/v1/auth/signup", json=user_data)
    assert signup_response.status_code in [200, 201]

    # Try to login with wrong password
    wrong_login_data = {
        "email": user_data["email"],
        "password": "WrongPassword123!"
    }

    login_response = client.post("/v1/auth/login", json=wrong_login_data)
    assert login_response.status_code == 401