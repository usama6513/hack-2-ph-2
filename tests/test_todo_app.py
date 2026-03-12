"""
Tests for Todo Console Application - Phase I

These tests validate the functionality of the TodoApp and Task classes
according to the Phase I specification and tasks.
"""

import pytest
from todo_app import TodoApp, Task


class TestTask:
    """Test the Task class functionality."""

    def test_task_creation_valid(self):
        """Test creating a valid Task instance."""
        task = Task(1, "Test task description")
        assert task.id == 1
        assert task.description == "Test task description"
        assert task.completed is False

    def test_task_creation_with_completion_status(self):
        """Test creating a Task with completion status."""
        task = Task(2, "Test task", True)
        assert task.id == 2
        assert task.description == "Test task"
        assert task.completed is True

    def test_task_creation_invalid_id(self):
        """Test creating a Task with invalid ID raises ValueError."""
        with pytest.raises(ValueError):
            Task(0, "Test task")

        with pytest.raises(ValueError):
            Task(-1, "Test task")

    def test_task_creation_invalid_description(self):
        """Test creating a Task with invalid description raises ValueError."""
        with pytest.raises(ValueError):
            Task(1, "")

        with pytest.raises(ValueError):
            Task(1, "   ")

        with pytest.raises(ValueError):
            Task(1, "")

    def test_task_str_representation(self):
        """Test the string representation of a Task."""
        task = Task(1, "Test task")
        assert str(task) == "[○] 1. Test task"

        task.completed = True
        assert str(task) == "[✓] 1. Test task"

    def test_task_to_dict(self):
        """Test the to_dict method of a Task."""
        task = Task(1, "Test task", True)
        expected_dict = {
            "id": 1,
            "description": "Test task",
            "completed": True
        }
        assert task.to_dict() == expected_dict


class TestTodoApp:
    """Test the TodoApp class functionality."""

    def test_initialization(self):
        """Test initializing TodoApp with empty task list."""
        app = TodoApp()
        assert len(app.tasks) == 0
        assert app.next_id == 1

    def test_add_task_valid(self):
        """Test adding a valid task."""
        app = TodoApp()
        task = app.add_task("New task")

        assert task is not None
        assert task.id == 1
        assert task.description == "New task"
        assert task.completed is False
        assert len(app.tasks) == 1
        assert 1 in app.tasks

    def test_add_task_empty_description(self):
        """Test adding a task with empty description returns None."""
        app = TodoApp()
        task = app.add_task("")

        assert task is None
        assert len(app.tasks) == 0

    def test_add_task_whitespace_description(self):
        """Test adding a task with whitespace-only description returns None."""
        app = TodoApp()
        task = app.add_task("   ")

        assert task is None
        assert len(app.tasks) == 0

    def test_list_tasks_empty(self):
        """Test listing tasks when task list is empty."""
        app = TodoApp()
        tasks = app.list_tasks()

        assert tasks == []

    def test_list_tasks_with_tasks(self):
        """Test listing tasks when task list has tasks."""
        app = TodoApp()
        app.add_task("Task 1")
        app.add_task("Task 2")

        tasks = app.list_tasks()
        assert len(tasks) == 2

        # Check that both tasks are in the list
        descriptions = [task.description for task in tasks]
        assert "Task 1" in descriptions
        assert "Task 2" in descriptions

    def test_get_task_exists(self):
        """Test getting a task that exists."""
        app = TodoApp()
        created_task = app.add_task("Test task")

        retrieved_task = app.get_task(created_task.id)
        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id
        assert retrieved_task.description == created_task.description
        assert retrieved_task.completed == created_task.completed

    def test_get_task_not_exists(self):
        """Test getting a task that does not exist."""
        app = TodoApp()
        app.add_task("Test task")

        retrieved_task = app.get_task(999)
        assert retrieved_task is None

    def test_update_task_exists(self):
        """Test updating a task that exists."""
        app = TodoApp()
        original_task = app.add_task("Original task")

        success = app.update_task(original_task.id, "Updated task")

        assert success is True
        assert original_task.description == "Updated task"

    def test_update_task_not_exists(self):
        """Test updating a task that does not exist."""
        app = TodoApp()
        app.add_task("Test task")

        success = app.update_task(999, "Updated task")

        assert success is False

    def test_update_task_empty_description(self):
        """Test updating a task with empty description."""
        app = TodoApp()
        original_task = app.add_task("Original task")

        success = app.update_task(original_task.id, "")

        assert success is False
        assert original_task.description == "Original task"  # Should remain unchanged

    def test_delete_task_exists(self):
        """Test deleting a task that exists."""
        app = TodoApp()
        task_to_delete = app.add_task("Task to delete")
        other_task = app.add_task("Other task")

        success = app.delete_task(task_to_delete.id)

        assert success is True
        assert task_to_delete.id not in app.tasks
        assert other_task.id in app.tasks
        assert len(app.tasks) == 1

    def test_delete_task_not_exists(self):
        """Test deleting a task that does not exist."""
        app = TodoApp()
        app.add_task("Test task")

        success = app.delete_task(999)

        assert success is False
        assert len(app.tasks) == 1

    def test_mark_task_complete_exists(self):
        """Test marking a task as complete."""
        app = TodoApp()
        task = app.add_task("Test task")

        success = app.mark_task_complete(task.id)

        assert success is True
        assert task.completed is True

    def test_mark_task_complete_not_exists(self):
        """Test marking a task as complete when task doesn't exist."""
        app = TodoApp()
        app.add_task("Test task")

        success = app.mark_task_complete(999)

        assert success is False

    def test_mark_task_incomplete_exists(self):
        """Test marking a task as incomplete."""
        app = TodoApp()
        task = app.add_task("Test task")
        # First mark as complete
        app.mark_task_complete(task.id)

        success = app.mark_task_incomplete(task.id)

        assert success is True
        assert task.completed is False

    def test_mark_task_incomplete_not_exists(self):
        """Test marking a task as incomplete when task doesn't exist."""
        app = TodoApp()
        app.add_task("Test task")

        success = app.mark_task_incomplete(999)

        assert success is False

    def test_get_next_id_sequential(self):
        """Test that get_next_id returns sequential IDs."""
        app = TodoApp()

        id1 = app.get_next_id()
        assert id1 == 1

        id2 = app.get_next_id()
        assert id2 == 2

        id3 = app.get_next_id()
        assert id3 == 3

    def test_get_next_id_with_deletions(self):
        """Test that get_next_id properly manages IDs when tasks are deleted."""
        app = TodoApp()
        task1 = app.add_task("Task 1")
        task2 = app.add_task("Task 2")
        task3 = app.add_task("Task 3")

        # Delete middle task
        app.delete_task(task2.id)

        # Next ID should be 4 (not 2)
        next_id = app.get_next_id()
        assert next_id == 4


class TestIntegration:
    """Integration tests for User Stories."""

    def test_user_story_1_add_task_functionality(self):
        """Integration test for User Story 1: Add New Tasks."""
        app = TodoApp()

        # Verify initially empty
        assert len(app.tasks) == 0

        # Add a new task
        task = app.add_task("Buy groceries")

        # Verify task was added correctly
        assert task is not None
        assert task.id == 1
        assert task.description == "Buy groceries"
        assert task.completed is False
        assert len(app.tasks) == 1

        # Verify task is accessible through get_task
        retrieved_task = app.get_task(1)
        assert retrieved_task is not None
        assert retrieved_task.description == "Buy groceries"

    def test_user_story_2_view_task_list_functionality(self):
        """Integration test for User Story 2: View Task List."""
        app = TodoApp()

        # Test viewing empty list
        tasks = app.list_tasks()
        assert tasks == []

        # Add tasks
        app.add_task("Task 1")
        app.add_task("Task 2")

        # Test viewing non-empty list
        tasks = app.list_tasks()
        assert len(tasks) == 2

        # Verify each task has required properties
        descriptions = []
        for task in tasks:
            assert hasattr(task, 'id')
            assert hasattr(task, 'description')
            assert hasattr(task, 'completed')
            descriptions.append(task.description)

        assert "Task 1" in descriptions
        assert "Task 2" in descriptions

    def test_user_story_3_update_task_functionality(self):
        """Integration test for User Story 3: Update Task Description."""
        app = TodoApp()

        # Add a task to update
        original_task = app.add_task("Original description")
        original_id = original_task.id

        # Update the task
        success = app.update_task(original_id, "Updated description")

        # Verify update was successful
        assert success is True
        assert original_task.description == "Updated description"

        # Verify the task still exists and has the same ID
        retrieved_task = app.get_task(original_id)
        assert retrieved_task is not None
        assert retrieved_task.id == original_id
        assert retrieved_task.description == "Updated description"

    def test_user_story_4_delete_task_functionality(self):
        """Integration test for User Story 4: Delete Task."""
        app = TodoApp()

        # Add tasks
        task_to_delete = app.add_task("Task to delete")
        other_task = app.add_task("Other task")

        # Delete the first task
        success = app.delete_task(task_to_delete.id)

        # Verify deletion was successful
        assert success is True
        assert len(app.tasks) == 1

        # Verify the right task was deleted
        assert task_to_delete.id not in app.tasks
        assert other_task.id in app.tasks

        # Verify the other task still exists
        retrieved_other_task = app.get_task(other_task.id)
        assert retrieved_other_task is not None
        assert retrieved_other_task.id == other_task.id

    def test_user_story_5_mark_task_complete_incomplete_functionality(self):
        """Integration test for User Story 5: Mark Task Complete/Incomplete."""
        app = TodoApp()

        # Add a task
        task = app.add_task("Test task")

        # Initially task should be incomplete
        assert task.completed is False

        # Mark task as complete
        success_complete = app.mark_task_complete(task.id)

        # Verify mark complete was successful
        assert success_complete is True
        assert task.completed is True

        # Mark task as incomplete
        success_incomplete = app.mark_task_incomplete(task.id)

        # Verify mark incomplete was successful
        assert success_incomplete is True
        assert task.completed is False


def test_empty_list_scenario():
    """Integration test for viewing empty list scenario from US2."""
    app = TodoApp()

    # Test that the list is empty initially
    tasks = app.list_tasks()
    assert len(tasks) == 0
    assert tasks == []


def test_invalid_task_id_scenarios():
    """Test scenarios with invalid task IDs from requirements."""
    app = TodoApp()

    # Add a task to have at least one valid ID
    app.add_task("Valid task")

    # Test operations with invalid task ID
    assert app.get_task(999) is None
    assert app.update_task(999, "New description") is False
    assert app.delete_task(999) is False
    assert app.mark_task_complete(999) is False
    assert app.mark_task_incomplete(999) is False