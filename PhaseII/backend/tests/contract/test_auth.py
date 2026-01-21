import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from unittest.mock import Mock

from src.main import app
from src.models.user import User, UserCreate
from src.database import engine
from src.services.auth import hash_password


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


def test_signup_endpoint_contract(client: TestClient, db_session: Session):
    """Test the /auth/signup endpoint contract."""
    # Test data
    user_data = {
        "email": "test@example.com",
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": "User"
    }

    # Send request
    response = client.post("/v1/auth/signup", json=user_data)

    # Verify response structure and status code
    assert response.status_code in [200, 201], f"Expected 200 or 201, got {response.status_code}"

    # Verify response contains expected fields
    response_data = response.json()
    assert "access_token" in response_data, "Response should contain access_token"
    assert "token_type" in response_data, "Response should contain token_type"
    assert "user" in response_data, "Response should contain user object"

    user_response = response_data["user"]
    assert "id" in user_response, "User response should contain id"
    assert user_response["email"] == user_data["email"], "Email should match input"
    assert user_response["first_name"] == user_data["first_name"], "First name should match input"
    assert user_response["last_name"] == user_data["last_name"], "Last name should match input"
    assert "created_at" in user_response, "User response should contain created_at"
    assert "updated_at" in user_response, "User response should contain updated_at"

    # Verify user was created in the database
    statement = select(User).where(User.email == user_data["email"])
    user_in_db = db_session.exec(statement).first()
    assert user_in_db is not None, "User should be created in the database"
    assert user_in_db.email == user_data["email"], "Stored email should match input"
    assert user_in_db.first_name == user_data["first_name"], "Stored first name should match input"
    assert user_in_db.last_name == user_data["last_name"], "Stored last name should match input"


def test_login_endpoint_contract(client: TestClient, db_session: Session):
    """Test the /auth/login endpoint contract."""
    # First, create a user directly in the database
    test_email = "login_test@example.com"
    test_password = "password123"

    user = User(
        email=test_email,
        password_hash=hash_password(test_password),
        first_name="Login",
        last_name="Test"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Test login with correct credentials
    login_data = {
        "email": test_email,
        "password": test_password
    }

    response = client.post("/v1/auth/login", json=login_data)

    # Verify response structure and status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Verify response contains expected fields
    response_data = response.json()
    assert "access_token" in response_data, "Response should contain access_token"
    assert "token_type" in response_data, "Response should contain token_type"
    assert "user" in response_data, "Response should contain user object"

    user_response = response_data["user"]
    assert "id" in user_response, "User response should contain id"
    assert user_response["email"] == test_email, "Email should match input"
    assert "created_at" in user_response, "User response should contain created_at"
    assert "updated_at" in user_response, "User response should contain updated_at"

    # Test login with incorrect credentials
    wrong_login_data = {
        "email": test_email,
        "password": "wrongpassword"
    }

    wrong_response = client.post("/v1/auth/login", json=wrong_login_data)
    assert wrong_response.status_code == 401, f"Expected 401 for wrong credentials, got {wrong_response.status_code}"