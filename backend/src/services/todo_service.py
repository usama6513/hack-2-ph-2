from sqlmodel import Session, select
from typing import List, Optional
from ..models.todo import Todo
from ..models.user import User

class TodoService:
    """
    Service class for todo-related operations.
    """

    @staticmethod
    def create_todo(todo_data: dict, user_id: int, db_session: Session) -> Todo:
        """
        Create a new todo for a user.
        """
        todo = Todo(
            description=todo_data["description"],
            completed=todo_data.get("completed", False),
            user_id=user_id
        )

        db_session.add(todo)
        db_session.commit()
        db_session.refresh(todo)

        return todo

    @staticmethod
    def get_todos_by_user(user_id: int, db_session: Session) -> List[Todo]:
        """
        Retrieve all todos for a specific user.
        """
        statement = select(Todo).where(Todo.user_id == user_id)
        return db_session.exec(statement).all()

    @staticmethod
    def get_todo_by_id(todo_id: int, user_id: int, db_session: Session) -> Optional[Todo]:
        """
        Retrieve a specific todo by ID for a user.
        """
        statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        return db_session.exec(statement).first()

    @staticmethod
    def update_todo(todo_id: int, user_id: int, update_data: dict, db_session: Session) -> Optional[Todo]:
        """
        Update a specific todo for a user.
        """
        todo = TodoService.get_todo_by_id(todo_id, user_id, db_session)
        if not todo:
            return None

        # Update the fields
        for field, value in update_data.items():
            if hasattr(todo, field):
                setattr(todo, field, value)

        db_session.add(todo)
        db_session.commit()
        db_session.refresh(todo)

        return todo

    @staticmethod
    def toggle_todo_status(todo_id: int, user_id: int, db_session: Session) -> Optional[Todo]:
        """
        Toggle the completion status of a specific todo for a user.
        """
        todo = TodoService.get_todo_by_id(todo_id, user_id, db_session)
        if not todo:
            return None

        todo.completed = not todo.completed

        db_session.add(todo)
        db_session.commit()
        db_session.refresh(todo)

        return todo

    @staticmethod
    def delete_todo(todo_id: int, user_id: int, db_session: Session) -> bool:
        """
        Delete a specific todo for a user.
        """
        todo = TodoService.get_todo_by_id(todo_id, user_id, db_session)
        if not todo:
            return False

        db_session.delete(todo)
        db_session.commit()

        return True