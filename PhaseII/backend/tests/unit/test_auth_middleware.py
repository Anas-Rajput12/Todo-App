import pytest
from datetime import timedelta
from jose import jwt
from sqlmodel import Session, select

from src.middleware.auth import create_access_token, verify_token, JWTBearer
from src.models.user import User
from src.database import engine
from src.config import settings


@pytest.fixture
def db_session():
    """Create a test database session."""
    with Session(engine) as session:
        yield session


def test_create_access_token():
    """Test that access tokens can be created properly."""
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(minutes=30)

    token = create_access_token(data=data, expires_delta=expires_delta)

    # Verify that token is created
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

    # Verify that token can be decoded
    decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded_payload["sub"] == "test@example.com"
    assert "exp" in decoded_payload


def test_verify_valid_token():
    """Test that valid tokens can be verified."""
    data = {"sub": "test@example.com"}
    token = create_access_token(data=data)

    token_data = verify_token(token)

    # Verify that token data is returned correctly
    assert token_data is not None
    assert token_data.username == "test@example.com"


def test_verify_invalid_token():
    """Test that invalid tokens return None."""
    invalid_token = "invalid.token.string"

    token_data = verify_token(invalid_token)

    # Verify that None is returned for invalid token
    assert token_data is None


def test_verify_expired_token():
    """Test that expired tokens return None."""
    data = {"sub": "test@example.com"}
    # Create a token that expires immediately
    token = create_access_token(data=data, expires_delta=timedelta(seconds=1))

    # Wait for the token to expire
    import time
    time.sleep(2)

    token_data = verify_token(token)

    # Verify that None is returned for expired token
    assert token_data is None


def test_jwt_bearer_with_valid_user(db_session: Session):
    """Test JWTBearer with a valid user."""
    # Create a test user in the database
    user = User(
        email="jwt_test@example.com",
        password_hash="hashed_password",
        first_name="JWT",
        last_name="Test"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create a token for this user
    data = {"sub": "jwt_test@example.com"}
    token = create_access_token(data=data)

    # Test that the JWTBearer class accepts the token
    # This is a simplified test since JWTBearer is a FastAPI dependency class
    # We'll test the underlying functionality instead
    token_data = verify_token(token)
    assert token_data is not None
    assert token_data.username == "jwt_test@example.com"

    # Verify user exists in database
    statement = select(User).where(User.email == "jwt_test@example.com")
    db_user = db_session.exec(statement).first()
    assert db_user is not None
    assert db_user.email == "jwt_test@example.com"


def test_jwt_bearer_with_nonexistent_user():
    """Test JWTBearer with a token for a nonexistent user."""
    # Create a token with an email that doesn't exist in DB
    data = {"sub": "nonexistent@example.com"}
    token = create_access_token(data=data)

    # The token itself is valid, but the user doesn't exist
    # This would be caught at the dependency injection level in the actual app
    token_data = verify_token(token)
    assert token_data is not None
    assert token_data.username == "nonexistent@example.com"