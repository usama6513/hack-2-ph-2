# FastAPI REST API Endpoints with User Isolation and Ownership Checks

## Overview
This skill provides a complete guide for building secure REST API endpoints in FastAPI with proper user isolation, ownership verification, and appropriate HTTP status codes. It includes CRUD operations templates with security patterns, error handling, and best practices for multi-tenant applications.

## Prerequisites
- Python 3.9+
- FastAPI
- SQLModel or SQLAlchemy
- python-jose[cryptography] for JWT operations (for authentication)
- pydantic for request/response models

## Project Structure
```
src/
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── user.py
│   └── todo.py
├── schemas/
│   ├── __init__.py
│   ├── todo.py
│   └── user.py
├── api/
│   ├── __init__.py
│   ├── deps.py
│   └── v1/
│       ├── __init__.py
│       ├── todos.py
│       └── users.py
├── core/
│   ├── __init__.py
│   └── security.py
└── database/
    ├── __init__.py
    └── session.py
```

## Base Models (src/models/base.py):
```python
from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BaseSQLModel(SQLModel):
    """Base SQLModel with common fields for all tables."""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class BaseResponse(BaseModel):
    """Base response model for all API responses."""
    success: bool
    message: str
    data: Optional[dict] = None
```

## User and Todo Models (src/models/user.py and src/models/todo.py):

### src/models/user.py:
```python
from sqlmodel import Field
from typing import Optional
from .base import BaseSQLModel


class User(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = True
```

### src/models/todo.py:
```python
from sqlmodel import Field, Relationship
from typing import Optional
from .base import BaseSQLModel
from .user import User


class Todo(BaseSQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = False
    user_id: int = Field(foreign_key="user.id", index=True)

    # Relationship to user
    user: User = Relationship(back_populates="todos")


# Back-populate the relationship in User model
User.model_rebuild()
```

## API Request/Response Schemas (src/schemas/todo.py):
```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TodoRead(TodoBase):
    id: int
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoReadWithUser(TodoRead):
    user_email: str
```

## Security Dependencies (src/api/deps.py):
```python
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
from ..database.session import get_session
from ..core.security import get_current_active_user
from ..models.user import User


def get_current_user_with_session(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
) -> tuple[User, Session]:
    """
    Dependency that provides both the current user and database session.
    """
    return current_user, session


def get_user_if_owner(
    user_id: int,
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Verify that the current user is the owner of a resource (by user ID).
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource"
        )
    return current_user
```

## Core Security (src/core/security.py):
```python
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
from sqlmodel import Session
from ..database.session import get_session
from ..models.user import User


# HTTP Bearer token scheme
security = HTTPBearer()


def verify_token(token: str) -> Optional[dict]:
    """
    Verify JWT token and return payload.
    """
    # Implementation depends on your JWT strategy
    # For Better Auth integration, use the shared secret
    from .config import settings

    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


async def get_current_active_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Get the current authenticated user from the JWT token.
    """
    payload = verify_token(credentials.credentials)
    user_id: int = int(payload.get("sub"))

    # You'll need to fetch the user from your database here
    # Implementation depends on your database setup
    from ..database.session import get_session
    from sqlmodel import select

    session = next(get_session())
    try:
        user = session.get(User, user_id)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        return user
    finally:
        session.close()
```

## Main API Endpoints (src/api/v1/todos.py):
```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session, select, update, delete
from ..deps import get_current_user_with_session
from ...models.todo import Todo
from ...models.user import User
from ...schemas.todo import TodoCreate, TodoRead, TodoUpdate, TodoReadWithUser
from ...database.session import get_session


router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate,
    current_data: tuple[User, Session] = Depends(get_current_user_with_session)
) -> TodoRead:
    """
    Create a new todo item for the current user.
    """
    current_user, session = current_data

    # Create the todo with the current user's ID
    db_todo = Todo(
        **todo.model_dump(),
        user_id=current_user.id
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get("/", response_model=List[TodoRead])
def read_todos(
    skip: int = 0,
    limit: int = 100,
    current_data: tuple[User, Session] = Depends(get_current_user_with_session)
) -> List[TodoRead]:
    """
    Retrieve all todos for the current user.
    """
    current_user, session = current_data

    # Only fetch todos that belong to the current user
    statement = (
        select(Todo)
        .where(Todo.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    todos = session.exec(statement).all()

    return todos


@router.get("/{todo_id}", response_model=TodoRead)
def read_todo(
    todo_id: int,
    current_data: tuple[User, Session] = Depends(get_current_user_with_session)
) -> TodoRead:
    """
    Get a specific todo by ID, ensuring it belongs to the current user.
    """
    current_user, session = current_data

    # Get the todo and verify ownership
    todo = session.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Verify that the todo belongs to the current user
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this todo"
        )

    return todo


@router.put("/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_data: tuple[User, Session] = Depends(get_current_user_with_session)
) -> TodoRead:
    """
    Update a todo, ensuring ownership.
    """
    current_user, session = current_data

    # Get the todo and verify ownership
    todo = session.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Verify that the todo belongs to the current user
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this todo"
        )

    # Update only the fields that are provided
    update_data = todo_update.model_dump(exclude_unset=True)

    # Update the todo
    for field, value in update_data.items():
        setattr(todo, field, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


@router.patch("/{todo_id}/status", response_model=TodoRead)
def update_todo_status(
    todo_id: int,
    completed: bool,
    current_data: tuple[User, Session] = Depends(get_current_user_with_session)
) -> TodoRead:
    """
    Update only the completion status of a todo, ensuring ownership.
    """
    current_user, session = current_data

    # Get the todo and verify ownership
    todo = session.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Verify that the todo belongs to the current user
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this todo"
        )

    # Update the completion status
    todo.completed = completed

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    current_data: tuple[User, Session] = Depends(get_current_user_with_session)
) -> None:
    """
    Delete a todo, ensuring ownership.
    """
    current_user, session = current_data

    # Get the todo and verify ownership
    todo = session.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Verify that the todo belongs to the current user
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this todo"
        )

    # Delete the todo
    session.delete(todo)
    session.commit()


# Additional utility endpoints
@router.get("/completed", response_model=List[TodoRead])
def read_completed_todos(
    current_data: tuple[User, Session] = Depends(get_current_user_with_session)
) -> List[TodoRead]:
    """
    Get all completed todos for the current user.
    """
    current_user, session = current_data

    statement = (
        select(Todo)
        .where(Todo.user_id == current_user.id)
        .where(Todo.completed == True)
    )
    todos = session.exec(statement).all()

    return todos


@router.get("/pending", response_model=List[TodoRead])
def read_pending_todos(
    current_data: tuple[User, Session] = Depends(get_current_user_with_session)
) -> List[TodoRead]:
    """
    Get all pending (not completed) todos for the current user.
    """
    current_user, session = current_data

    statement = (
        select(Todo)
        .where(Todo.user_id == current_user.id)
        .where(Todo.completed == False)
    )
    todos = session.exec(statement).all()

    return todos
```

## Database Session Management (src/database/session.py):
```python
from sqlmodel import create_engine, Session
from typing import Generator
from ..core.config import settings


# Create database engine
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+asyncpg"
)

engine = create_engine(
    connection_string,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to provide database session.
    """
    with Session(engine) as session:
        yield session
```

## HTTP Status Code Best Practices

### Standard Status Codes for CRUD Operations:
- **GET /todos/**: 200 OK
- **GET /todos/{id}**: 200 OK, 404 Not Found
- **POST /todos/**: 201 Created
- **PUT /todos/{id}**: 200 OK, 404 Not Found, 403 Forbidden
- **PATCH /todos/{id}**: 200 OK, 404 Not Found, 403 Forbidden
- **DELETE /todos/{id}**: 204 No Content, 404 Not Found, 403 Forbidden

### Security-Related Status Codes:
- **401 Unauthorized**: Invalid or missing authentication token
- **403 Forbidden**: User not authorized to access resource (ownership check failed)
- **404 Not Found**: Resource doesn't exist (don't reveal if resource exists if user doesn't own it)

## Error Handling Best Practices

### 1. Consistent Error Responses:
```python
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation error",
            "data": {"errors": exc.errors()}
        }
    )
```

### 2. Ownership Check Patterns:
```python
def verify_ownership(
    session: Session,
    model_class,
    resource_id: int,
    user_id: int
) -> bool:
    """
    Generic function to verify ownership of a resource.
    """
    resource = session.get(model_class, resource_id)
    if not resource:
        return False

    # Assume the resource has a user_id field
    return hasattr(resource, 'user_id') and resource.user_id == user_id
```

### 3. Response Model Consistency:
```python
from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    error: Optional[str] = None
```

## Testing Examples

### Unit Tests:
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database.session import get_session
from src.models.user import User
from src.models.todo import Todo


# Override the database session for testing
@pytest.fixture
def override_get_session():
    # Create an in-memory database for testing
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables
    from src.models.base import SQLModel
    SQLModel.metadata.create_all(bind=engine)

    def get_session_override():
        try:
            session = TestingSessionLocal()
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_session] = get_session_override
    yield TestingSessionLocal()
    app.dependency_overrides.clear()


def test_create_todo_success(override_get_session):
    client = TestClient(app)

    # Mock authenticated user
    # (Implementation depends on your authentication setup)

    response = client.post(
        "/api/v1/todos/",
        json={"title": "Test Todo", "description": "Test description"},
        headers={"Authorization": "Bearer valid_token"}
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Test Todo"


def test_read_todos_ownership(override_get_session):
    client = TestClient(app)

    # Create a todo owned by user 1
    # (Implementation depends on your test setup)

    response = client.get(
        "/api/v1/todos/1",
        headers={"Authorization": "Bearer token_for_user_2"}  # Different user
    )

    assert response.status_code == 403  # Forbidden - not owner
```

This comprehensive skill provides everything needed to build secure, properly isolated REST API endpoints in FastAPI with appropriate HTTP status codes and ownership verification.