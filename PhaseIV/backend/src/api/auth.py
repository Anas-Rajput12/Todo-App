from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import ValidationError, EmailStr
from typing import Dict, Any
import re
from datetime import timedelta, datetime
from collections import defaultdict
import time

from ..database import get_session
from ..models.user import UserCreate, UserRead
from ..services.auth import create_user, authenticate_user
from ..middleware.auth import create_access_token, JWTBearer
from ..utils.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from ..utils.logging_config import setup_logging

# Set up logging
logger = setup_logging()

router = APIRouter()

# Rate limiting storage (in production, use Redis or similar)
login_attempts = defaultdict(list)  # ip_address -> list of timestamps
registration_attempts = defaultdict(list)  # ip_address -> list of timestamps

# Rate limiting constants
LOGIN_RATE_LIMIT = 5  # Max attempts
LOGIN_TIME_WINDOW = 300  # 5 minutes in seconds
REGISTRATION_RATE_LIMIT = 3  # Max attempts
REGISTRATION_TIME_WINDOW = 3600  # 1 hour in seconds


def validate_email_format(email: str) -> bool:
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> list:
    """Validate password strength and return list of validation errors."""
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")

    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")

    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")

    if not re.search(r'\d', password):
        errors.append("Password must contain at least one digit")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")

    return errors


def check_rate_limit(attempts_dict: defaultdict, ip_address: str, max_attempts: int, time_window: int) -> bool:
    """
    Check if the IP address has exceeded the rate limit.

    Args:
        attempts_dict: Dictionary storing attempts by IP
        ip_address: The IP address to check
        max_attempts: Maximum number of attempts allowed
        time_window: Time window in seconds

    Returns:
        bool: True if rate limit is exceeded, False otherwise
    """
    now = time.time()
    # Remove attempts older than the time window
    attempts_dict[ip_address] = [timestamp for timestamp in attempts_dict[ip_address]
                                 if now - timestamp < time_window]

    # Check if we're over the limit
    if len(attempts_dict[ip_address]) >= max_attempts:
        return True

    # Add current attempt
    attempts_dict[ip_address].append(now)
    return False


@router.post("/signup", response_model=Dict[str, Any])
def register_user(
    user_create: UserCreate,
    session: Session = Depends(get_session),
    x_forwarded_for: str = None  # Get client IP from header
):
    """
    Register a new user.

    Args:
        user_create: User creation data
        session: Database session
        x_forwarded_for: Client IP address (from header)

    Returns:
        Dict: Access token and user information
    """
    # Get client IP for rate limiting
    client_ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else "unknown"

    # Check rate limit for registration
    if check_rate_limit(registration_attempts, client_ip, REGISTRATION_RATE_LIMIT, REGISTRATION_TIME_WINDOW):
        logger.warning(f"Rate limit exceeded for registration from IP: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many registration attempts. Please try again later."
        )

    try:
        # Comprehensive input validation
        if not user_create.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is required"
            )

        if not validate_email_format(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )

        if not user_create.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is required"
            )

        password_errors = validate_password_strength(user_create.password)
        if password_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password validation failed: " + "; ".join(password_errors)
            )

        # Sanitize user input - strip whitespace
        user_create.email = user_create.email.strip().lower()
        if hasattr(user_create, 'first_name') and user_create.first_name:
            user_create.first_name = user_create.first_name.strip()[:50]  # Limit length
        if hasattr(user_create, 'last_name') and user_create.last_name:
            user_create.last_name = user_create.last_name.strip()[:50]    # Limit length

        # Create the user in the database
        user = create_user(session, user_create)

        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        logger.info(f"Successfully registered new user: {user.email} from IP: {client_ip}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    except UserAlreadyExistsException:
        logger.warning(f"Registration attempt with existing email: {user_create.email} from IP: {client_ip}")
        raise
    except HTTPException:
        logger.warning(f"HTTP exception during registration: {user_create.email} from IP: {client_ip}")
        raise
    except ValidationError as ve:
        logger.error(f"Validation error during registration: {ve.errors()}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {ve.errors()}"
        )
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during registration"
        )


@router.post("/login", response_model=Dict[str, Any])
def login_user(
    user_credentials: UserCreate,
    session: Session = Depends(get_session),
    x_forwarded_for: str = None  # Get client IP from header
):
    """
    Authenticate user and return access token.

    Args:
        user_credentials: User credentials (email and password)
        session: Database session
        x_forwarded_for: Client IP address (from header)

    Returns:
        Dict: Access token and user information
    """
    # Get client IP for rate limiting
    client_ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else "unknown"

    # Check rate limit for login attempts
    if check_rate_limit(login_attempts, client_ip, LOGIN_RATE_LIMIT, LOGIN_TIME_WINDOW):
        logger.warning(f"Rate limit exceeded for login from IP: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later."
        )

    try:
        # Validate input data
        if not user_credentials.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is required"
            )

        if not validate_email_format(user_credentials.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )

        if not user_credentials.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is required"
            )

        # Sanitize user input - strip whitespace
        email = user_credentials.email.strip().lower()

        user = authenticate_user(
            session=session,
            email=email,
            password=user_credentials.password
        )

        if not user:
            logger.warning(f"Failed login attempt for email: {email} from IP: {client_ip}")
            raise InvalidCredentialsException()

        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        logger.info(f"Successful login for user: {email} from IP: {client_ip}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    except InvalidCredentialsException:
        # Re-raise the known exception
        raise
    except HTTPException:
        logger.warning(f"HTTP exception during login: {user_credentials.email if user_credentials.email else 'unknown'} from IP: {client_ip}")
        raise
    except ValidationError as ve:
        logger.error(f"Validation error during login: {ve.errors()}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {ve.errors()}"
        )
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during login"
        )


@router.get("/profile", response_model=UserRead)
def get_profile(current_user: UserRead = Depends(JWTBearer())):
    """
    Get the current user's profile.

    Args:
        current_user: The currently authenticated user (extracted from JWT)

    Returns:
        UserRead: The current user's information
    """
    try:
        if not current_user:
            logger.warning("Attempt to access profile without authentication")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )

        logger.info(f"Profile accessed for user: {current_user.email}")
        return current_user
    except HTTPException:
        logger.warning("HTTP exception during profile access")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during profile access: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving profile"
        )