import logging
from sqlmodel import Session, select
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError

from ..models.user import User, UserCreate
from ..utils.exceptions import UserAlreadyExistsException, UserNotFoundException, InvalidCredentialsException
from ..config import settings


# Set up logger
logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password to compare against

    Returns:
        bool: True if the passwords match, False otherwise
    """
    verified = pwd_context.verify(plain_password, hashed_password)
    logger.debug(f"Password verification {'succeeded' if verified else 'failed'} for email")
    return verified


def get_password_hash(password: str) -> str:
    """
    Generate a hash for a plain password.

    Args:
        password: The plain text password to hash

    Returns:
        str: The hashed password
    """
    hashed = pwd_context.hash(password)
    logger.debug("Password hashed successfully")
    return hashed


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.

    Args:
        session: Database session
        email: User's email address
        password: User's plain text password

    Returns:
        User: The authenticated user if credentials are valid, None otherwise
    """
    logger.info(f"Attempting to authenticate user with email: {email}")

    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user:
        logger.warning(f"Authentication failed: User with email {email} not found")
        return None

    if not verify_password(password, user.password_hash):
        logger.warning(f"Authentication failed: Incorrect password for user {email}")
        return None

    logger.info(f"Successfully authenticated user: {email}")
    return user


def create_user(session: Session, user_create: UserCreate) -> User:
    """
    Create a new user in the database.

    Args:
        session: Database session
        user_create: User creation data

    Returns:
        User: The created user

    Raises:
        UserAlreadyExistsException: If a user with the email already exists
    """
    logger.info(f"Creating new user with email: {user_create.email}")

    # Check if user already exists
    statement = select(User).where(User.email == user_create.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        logger.warning(f"User creation failed: User with email {user_create.email} already exists")
        raise UserAlreadyExistsException(email=user_create.email)

    # Create new user
    user = User(
        email=user_create.email,
        password_hash=get_password_hash(user_create.password),
        first_name=user_create.first_name,
        last_name=user_create.last_name,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    logger.info(f"Successfully created user with email: {user_create.email}")
    return user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """
    Get a user by their email address.

    Args:
        session: Database session
        email: User's email address

    Returns:
        User: The user if found, None otherwise
    """
    logger.debug(f"Retrieving user by email: {email}")

    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if user:
        logger.debug(f"User found for email: {email}")
    else:
        logger.debug(f"No user found for email: {email}")

    return user