# FastAPI Backend Setup with SQLModel and Neon PostgreSQL

## Overview
This skill provides a complete setup for a FastAPI backend application with SQLModel for database modeling and Neon PostgreSQL as the database. It follows industry best practices for project structure, database connection management, and environment configuration.

## Prerequisites
- Python 3.9+
- pip
- uv (optional but recommended as a fast alternative to pip)

## Installation

### Using pip:
```bash
pip install "fastapi[all]" sqlmodel asyncpg python-dotenv uvicorn
```

### Using uv (recommended):
```bash
uv pip install "fastapi[all]" sqlmodel asyncpg python-dotenv uvicorn
```

## Project Structure

Recommended project structure:
```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── user.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── users.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── session.py
│   └── core/
│       ├── __init__.py
│       └── config.py
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── alembic.ini
```

## Environment Configuration

### .env file:
```bash
# Database
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
DATABASE_URL_TEST=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname_test

# FastAPI
API_V1_STR=/api/v1
PROJECT_NAME=MyProject

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

### .env.example file:
```bash
# Database
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
DATABASE_URL_TEST=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname_test

# FastAPI
API_V1_STR=/api/v1
PROJECT_NAME=MyProject

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

## Core Configuration Files

### src/core/config.py
```python
from pydantic_settings import Settings
from typing import List, Union


class Settings(Settings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MyProject"

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = []

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

### src/database/session.py
```python
from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool
from .config import settings


# For Neon PostgreSQL, we use asyncpg as the async driver
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+asyncpg"
)

engine = create_engine(
    connection_string,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
)


def get_session():
    with Session(engine) as session:
        yield session
```

### src/models/base.py
```python
from sqlmodel import SQLModel
from typing import Optional
from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
```

### src/models/user.py
```python
from sqlmodel import SQLModel, Field, Column, DateTime
from typing import Optional
from datetime import datetime
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class User(UserBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
```

### src/main.py
```python
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.users import router as users_router
from .database.session import engine
from sqlmodel import SQLModel


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    origins = settings.BACKEND_CORS_ORIGINS
    if isinstance(origins, str):
        origins = [origins]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API routers
app.include_router(users_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    # Create database tables
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"message": "FastAPI Backend with SQLModel and Neon PostgreSQL"}
```

## Alembic Setup

### requirements.txt
```txt
fastapi[all]>=0.104.1
sqlmodel>=0.0.8
asyncpg>=0.29.0
python-dotenv>=1.0.0
uvicorn[standard]>=0.24.0
alembic>=1.12.0
pydantic-settings>=2.0.3
```

### alembic.ini
```ini
[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
# for all available tokens
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d%%(second).2d_%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding `alembic[tz]` to the pip requirements
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# max_length = 40

# version_num, used in the revision row
version_num = true

# version_path_separator, One of "space", "dot" or "underline"
# defaults to "underline"
version_path_separator = underline

# version_locations, list of paths where to store version files
# version_locations = %(here)s/bar %(here)s/bat alembic/versions

# version_locations, list of paths where to store version files
version_locations = %(here)s/alembic/versions

# The file extensions that script.py.mako will be written as
output_encoding = utf-8

sqlalchemy.url =
```

### alembic/env.py
```python
import sys
import os
from pathlib import Path

# Add the src directory to path so we can import our models
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from models.user import User  # Import your models
from database.session import connection_string

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata
from sqlmodel import SQLModel
target_metadata = SQLModel.metadata

config.set_main_option('sqlalchemy.url', connection_string)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## Running Migrations

### Initialize Alembic (first time only):
```bash
alembic init alembic
```

### Generate a migration:
```bash
alembic revision --autogenerate -m "Create user table"
```

### Run migrations:
```bash
alembic upgrade head
```

## Running the Application

### Using uvicorn:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Using the new FastAPI CLI (if using FastAPI 0.103+):
```bash
fastapi dev src/main.py
```

## Best Practices Summary

1. **Security**:
   - Use environment variables for secrets
   - Implement proper CORS configuration
   - Use password hashing
   - Implement proper authentication and authorization

2. **Database**:
   - Use connection pooling
   - Implement proper session management
   - Use migrations for schema management
   - Consider Neon's serverless features for scaling

3. **Performance**:
   - Use async/await throughout
   - Implement proper caching when needed
   - Use uv for faster package installation
   - Consider connection recycle settings for Neon

4. **Code Organization**:
   - Follow the project structure outlined
   - Separate concerns (models, API, database, core)
   - Use dependency injection
   - Implement proper error handling