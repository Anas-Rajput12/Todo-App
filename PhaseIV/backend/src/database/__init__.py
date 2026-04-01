from sqlmodel import create_engine, Session
from typing import Generator
from .config import DATABASE_URL

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for dependency injection.

    Yields:
        Session: A database session
    """
    with Session(engine) as session:
        yield session