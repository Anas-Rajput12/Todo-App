import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from src.main import app
from src.models.user import User
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


@pytest.fixture
def authenticated_client(client: TestClient, db_session: Session):
    """Create a client with an authenticated user."""
    # Create a test user
    user = User(
        email="jwt_test@example.com",
        password_hash=hash_password("securepassword123"),
        first_name="JWT",
        last_name="Test"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Login to get a token
    login_response = client.post("/v1/auth/login", json={
        "email": "jwt_test@example.com",
        "password": "securepassword123"
    })

    token = login_response.json()["access_token"]

    # Add the token to the client headers
    client.headers.update({"Authorization": f"Bearer {token}"})

    yield client, user

    # Cleanup
    client.headers.pop("Authorization", None)


def test_protected_routes_require_jwt_authentication(client: TestClient):
    """Test that protected routes require JWT authentication."""
    # Try to access a protected task route without JWT
    response = client.get("/v1/tasks/")

    # Should return 401 Unauthorized
    assert response.status_code == 401

    # Verify the error message indicates auth is required
    response_data = response.json()
    assert "detail" in response_data


def test_protected_routes_reject_invalid_jwt(client: TestClient):
    """Test that protected routes reject invalid JWT tokens."""
    # Set an invalid JWT token
    client.headers.update({"Authorization": "Bearer invalid.jwt.token"})

    # Try to access a protected task route
    response = client.get("/v1/tasks/")

    # Should return 401 Unauthorized
    assert response.status_code == 401

    # Remove the invalid token
    client.headers.pop("Authorization", None)


def test_protected_routes_accept_valid_jwt(authenticated_client):
    """Test that protected routes accept valid JWT tokens."""
    client, user = authenticated_client

    # Try to access a protected task route with valid JWT
    response = client.get("/v1/tasks/")

    # Should return 200 OK
    assert response.status_code == 200


def test_auth_routes_dont_require_jwt(client: TestClient):
    """Test that authentication routes don't require JWT tokens."""
    # Try to access auth routes without JWT
    response = client.get("/health")

    # Should return 200 OK
    assert response.status_code == 200


def test_jwt_missing_prefix(client: TestClient):
    """Test that JWT enforcement rejects tokens without 'Bearer' prefix."""
    # Set a JWT token without the Bearer prefix
    client.headers.update({"Authorization": "invalidtokenwithoutprefix"})

    # Try to access a protected task route
    response = client.get("/v1/tasks/")

    # Should return 401 Unauthorized
    assert response.status_code == 401

    # Remove the invalid token
    client.headers.pop("Authorization", None)


def test_jwt_malformed_token(client: TestClient):
    """Test that JWT enforcement rejects malformed tokens."""
    # Set a malformed JWT token
    client.headers.update({"Authorization": "Bearer malformed.token"})

    # Try to access a protected task route
    response = client.get("/v1/tasks/")

    # Should return 401 Unauthorized
    assert response.status_code == 401

    # Remove the invalid token
    client.headers.pop("Authorization", None)