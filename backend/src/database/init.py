from sqlmodel import Session
from typing import Generator
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine
# Use connect_args={"check_same_thread": False} for SQLite to allow multiple threads
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """
    Create database tables for all models.
    """
    # Import models here to avoid circular import issues
    from ..models.user import User
    from ..models.todo import Todo
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """
    Get database session for dependency injection.
    """
    with Session(engine) as session:
        yield session