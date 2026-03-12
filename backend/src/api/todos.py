from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from typing import List, Optional, Dict
from jose import JWTError, jwt
from ..database.init import get_session
from ..models.todo import Todo
from ..models.user import User
from ..services.todo_service import TodoService
from ..services.user_service import UserService

from dotenv import load_dotenv
import os

load_dotenv()

# JWT configuration (should match auth.py)
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key-change-in-production")
ALGORITHM = "HS256"

router = APIRouter()

def get_current_user(token: str = Header(..., alias="authorization")) -> int:
    """
    Get current user ID from JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Remove "Bearer " prefix if present
        if token.startswith("Bearer "):
            token = token[7:]

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return int(user_id)

@router.get("/", response_model=List[Dict])
def get_todos(current_user_id: int = Depends(get_current_user), db: Session = Depends(get_session)):
    """
    Retrieve all todos for the authenticated user.
    """
    todos = TodoService.get_todos_by_user(current_user_id, db)

    return [
        {
            "id": todo.id,
            "description": todo.description,
            "completed": todo.completed,
            "user_id": todo.user_id,
            "created_at": todo.created_at,
            "updated_at": todo.updated_at
        }
        for todo in todos
    ]

@router.post("/", response_model=Dict)
def create_todo(todo_data: Dict[str, str], current_user_id: int = Depends(get_current_user), db: Session = Depends(get_session)):
    """
    Create a new todo for the authenticated user.
    """
    if not todo_data.get("description") or len(todo_data["description"].strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description is required"
        )

    todo = TodoService.create_todo(todo_data, current_user_id, db)

    return {
        "id": todo.id,
        "description": todo.description,
        "completed": todo.completed,
        "user_id": todo.user_id,
        "created_at": todo.created_at,
        "updated_at": todo.updated_at
    }

@router.put("/{todo_id}", response_model=Dict)
def update_todo(todo_id: int, update_data: Dict[str, str], current_user_id: int = Depends(get_current_user), db: Session = Depends(get_session)):
    """
    Update a specific todo for the authenticated user.
    """
    todo = TodoService.update_todo(todo_id, current_user_id, update_data, db)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return {
        "id": todo.id,
        "description": todo.description,
        "completed": todo.completed,
        "user_id": todo.user_id,
        "created_at": todo.created_at,
        "updated_at": todo.updated_at
    }

@router.patch("/{todo_id}/status", response_model=Dict)
def toggle_todo_status(todo_id: int, current_user_id: int = Depends(get_current_user), db: Session = Depends(get_session)):
    """
    Toggle the completion status of a specific todo for the authenticated user.
    """
    todo = TodoService.toggle_todo_status(todo_id, current_user_id, db)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return {
        "id": todo.id,
        "description": todo.description,
        "completed": todo.completed,
        "user_id": todo.user_id,
        "created_at": todo.created_at,
        "updated_at": todo.updated_at
    }

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, current_user_id: int = Depends(get_current_user), db: Session = Depends(get_session)):
    """
    Delete a specific todo for the authenticated user.
    """
    success = TodoService.delete_todo(todo_id, current_user_id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return {"message": "Todo deleted successfully"}