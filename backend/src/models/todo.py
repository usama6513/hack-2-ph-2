from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .user import User

class Todo(SQLModel, table=True):
    """
    Todo model representing a single todo item associated with a user.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    completed: bool = False
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="todos")