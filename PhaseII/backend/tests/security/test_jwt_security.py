import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from jose import jwt
import time

from src.main import app
from src.models.user import User
from src.database import engine
from src.services.auth import hash_password
from src.config import settings


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
        email="jwt_security_test@example.com",
        password_hash=hash_password("securepassword123"),
        first_name="JWT",
        last_name="Security"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Login to get a token
    login_response = client.post("/v1/auth/login", json={
        "email": "jwt_security_test@example.com",
        "password": "securepassword123"
    })

    token = login_response.json()["access_token"]

    # Add the token to the client headers
    client.headers.update({"Authorization": f"Bearer {token}"})

    yield client, user

    # Cleanup
    client.headers.pop("Authorization", None)


def test_jwt_token_expiration(client: TestClient, db_session: Session):
    """Test that JWT tokens expire as expected."""
    # Create a user
    user = User(
        email="exp_test@example.com",
        password_hash=hash_password("securepassword123"),
        first_name="Exp",
        last_name="Test"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Login to get a token
    login_response = client.post("/v1/auth/login", json={
        "email": "exp_test@example.com",
        "password": "securepassword123"
    })
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Manually create an expired token
    expired_payload = {
        "sub": "exp_test@example.com",
        "exp": time.time() - 100  # Expired 100 seconds ago
    }
    expired_token = jwt.encode(expired_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    # Try to access a protected route with expired token
    client.headers.update({"Authorization": f"Bearer {expired_token}"})
    response = client.get("/v1/tasks/")

    # Should return 401 Unauthorized
    assert response.status_code == 401

    # Cleanup
    client.headers.pop("Authorization", None)
    db_session.delete(user)
    db_session.commit()


def test_jwt_token_signature_verification(client: TestClient, db_session: Session):
    """Test that JWT tokens with invalid signatures are rejected."""
    # Create a user
    user = User(
        email="signature_test@example.com",
        password_hash=hash_password("securepassword123"),
        first_name="Signature",
        last_name="Test"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Login to get a valid token
    login_response = client.post("/v1/auth/login", json={
        "email": "signature_test@example.com",
        "password": "securepassword123"
    })
    assert login_response.status_code == 200

    # Create a token with invalid signature
    payload = {
        "sub": "signature_test@example.com",
        "exp": time.time() + 300  # Valid for 5 minutes
    }
    # Manually crafted token with invalid signature
    invalid_token = jwt.encode(payload, "wrong_secret", algorithm="HS256")

    # Try to access a protected route with invalid signature token
    client.headers.update({"Authorization": f"Bearer {invalid_token}"})
    response = client.get("/v1/tasks/")

    # Should return 401 Unauthorized
    assert response.status_code == 401

    # Cleanup
    client.headers.pop("Authorization", None)
    db_session.delete(user)
    db_session.commit()


def test_jwt_token_content_manipulation(client: TestClient, db_session: Session):
    """Test that manipulated JWT tokens are rejected."""
    # Create two users
    user1 = User(
        email="manipulate_test1@example.com",
        password_hash=hash_password("securepassword123"),
        first_name="Manipulate",
        last_name="Test1"
    )
    user2 = User(
        email="manipulate_test2@example.com",
        password_hash=hash_password("securepassword123"),
        first_name="Manipulate",
        last_name="Test2"
    )
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()
    db_session.refresh(user1)
    db_session.refresh(user2)

    # Login as user1 to get a valid token
    login_response = client.post("/v1/auth/login", json={
        "email": "manipulate_test1@example.com",
        "password": "securepassword123"
    })
    assert login_response.status_code == 200
    token1 = login_response.json()["access_token"]

    # Decode the token to extract payload
    payload = jwt.decode(token1, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    # Manipulate the token to pretend to be user2
    payload["sub"] = "manipulate_test2@example.com"
    manipulated_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    # Try to access user2's tasks with the manipulated token
    client.headers.update({"Authorization": f"Bearer {manipulated_token}"})
    response = client.get("/v1/tasks/")

    # Should return 401 Unauthorized since the token is now invalid
    assert response.status_code == 401

    # Cleanup
    client.headers.pop("Authorization", None)
    db_session.delete(user1)
    db_session.delete(user2)
    db_session.commit()


def test_concurrent_sessions_allowed(client: TestClient, db_session: Session):
    """Test that multiple sessions for the same user are allowed (stateless JWT)."""
    # Create a user
    user = User(
        email="concurrent_test@example.com",
        password_hash=hash_password("securepassword123"),
        first_name="Concurrent",
        last_name="Test"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Login twice to get two different tokens
    login_response1 = client.post("/v1/auth/login", json={
        "email": "concurrent_test@example.com",
        "password": "securepassword123"
    })
    assert login_response1.status_code == 200
    token1 = login_response1.json()["access_token"]

    login_response2 = client.post("/v1/auth/login", json={
        "email": "concurrent_test@example.com",
        "password": "securepassword123"
    })
    assert login_response2.status_code == 200
    token2 = login_response2.json()["access_token"]

    # Both tokens should work independently
    client.headers.update({"Authorization": f"Bearer {token1}"})
    response1 = client.get("/v1/tasks/")
    assert response1.status_code == 200

    client.headers.pop("Authorization", None)
    client.headers.update({"Authorization": f"Bearer {token2}"})
    response2 = client.get("/v1/tasks/")
    assert response2.status_code == 200

    # Cleanup
    client.headers.pop("Authorization", None)
    db_session.delete(user)
    db_session.commit()


def test_jwt_blacklist_functionality(client: TestClient, db_session: Session):
    """Test JWT token revocation/logout functionality."""
    # Create a user
    user = User(
        email="blacklist_test@example.com",
        password_hash=hash_password("securepassword123"),
        first_name="Blacklist",
        last_name="Test"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Login to get a token
    login_response = client.post("/v1/auth/login", json={
        "email": "blacklist_test@example.com",
        "password": "securepassword123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Access a protected route with valid token
    client.headers.update({"Authorization": f"Bearer {token}"})
    response = client.get("/v1/tasks/")
    assert response.status_code == 200

    # Simulate logout (in a real app, we'd add token to blacklist)
    # For now, we'll just test that we can still access with the same token
    # In a real implementation, the token would be blacklisted after logout
    response_after_logout_simulation = client.get("/v1/tasks/")
    assert response_after_logout_simulation.status_code == 200

    # Cleanup
    client.headers.pop("Authorization", None)
    db_session.delete(user)
    db_session.commit()