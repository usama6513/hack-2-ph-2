#!/usr/bin/env python3
"""
Todo Console Application - Phase I

A simple in-memory todo list application with a menu-driven CLI interface.
Features include adding, viewing, updating, deleting, and marking tasks as complete/incomplete.
"""

from typing import Dict, Optional


class Task:
    """Represents a single todo item in the application."""

    def __init__(self, task_id: int, description: str, completed: bool = False):
        """
        Initialize a Task instance.

        Args:
            task_id (int): Unique identifier for the task
            description (str): Text description of the task
            completed (bool): Status indicating whether the task is completed
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("task_id must be a positive integer")
        if not description or not isinstance(description, str) or not description.strip():
            raise ValueError("description must be a non-empty string")

        self.id = task_id
        self.description = description.strip()
        self.completed = completed

    def __str__(self) -> str:
        """Return a string representation of the task."""
        status = "X" if self.completed else "O"
        return f"[{status}] {self.id}. {self.description}"

    def to_dict(self) -> Dict:
        """Return a dictionary representation of the task."""
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed
        }


class TodoApp:
    """Main application class managing tasks and user interface."""

    def __init__(self):
        """Initialize the application with an empty task list and ID counter."""
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1

    def get_next_id(self) -> int:
        """Generate the next available unique ID for tasks."""
        current_id = self.next_id
        while current_id in self.tasks:
            current_id += 1
        self.next_id = current_id + 1
        return current_id

    def add_task(self, description: str) -> Optional[Task]:
        """
        Add a new task to the list.

        Args:
            description (str): The description of the task

        Returns:
            Task: The created task, or None if description is invalid
        """
        if not description or not description.strip():
            return None

        task_id = self.get_next_id()
        task = Task(task_id, description.strip())
        self.tasks[task_id] = task
        return task

    def list_tasks(self) -> list:
        """Return a list of all tasks."""
        return list(self.tasks.values())

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task: The task with the given ID, or None if not found
        """
        return self.tasks.get(task_id)

    def update_task(self, task_id: int, new_description: str) -> bool:
        """
        Update the description of an existing task.

        Args:
            task_id (int): The ID of the task to update
            new_description (str): The new description

        Returns:
            bool: True if update was successful, False otherwise
        """
        if task_id not in self.tasks:
            return False

        if not new_description or not new_description.strip():
            return False

        self.tasks[task_id].description = new_description.strip()
        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        if task_id not in self.tasks:
            return False

        del self.tasks[task_id]
        # Update next_id if necessary to prevent ID gaps
        if task_id == (self.next_id - 1):
            self.next_id = task_id
        return True

    def mark_task_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete.

        Args:
            task_id (int): The ID of the task to mark complete

        Returns:
            bool: True if marking was successful, False otherwise
        """
        if task_id not in self.tasks:
            return False

        self.tasks[task_id].completed = True
        return True

    def mark_task_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete.

        Args:
            task_id (int): The ID of the task to mark incomplete

        Returns:
            bool: True if marking was successful, False otherwise
        """
        if task_id not in self.tasks:
            return False

        self.tasks[task_id].completed = False
        return True

    def display_menu(self):
        """Display the main menu options to the user."""
        print("\n" + "="*40)
        print("TODO APPLICATION - MAIN MENU")
        print("="*40)
        print("1. Add a new task")
        print("2. View all tasks")
        print("3. Update a task")
        print("4. Delete a task")
        print("5. Mark task as complete")
        print("6. Mark task as incomplete")
        print("7. Exit")
        print("="*40)

    def get_user_choice(self) -> str:
        """Get and validate user menu choice."""
        try:
            choice = input("Enter your choice (1-7): ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\n\nApplication interrupted. Exiting...")
            return "7"

    def run(self):
        """Main application loop."""
        print("Welcome to the Todo Application!")
        print("Type '7' or 'exit' at any time to quit.")

        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.handle_add_task()
            elif choice == "2":
                self.handle_view_tasks()
            elif choice == "3":
                self.handle_update_task()
            elif choice == "4":
                self.handle_delete_task()
            elif choice == "5":
                self.handle_mark_complete()
            elif choice == "6":
                self.handle_mark_incomplete()
            elif choice == "7":
                self.handle_exit()
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

    def handle_add_task(self):
        """Handle adding a new task."""
        print("\n--- Add New Task ---")
        description = input("Enter task description: ").strip()

        if not description:
            print("Error: Task description cannot be empty.")
            return

        task = self.add_task(description)
        if task:
            print(f"Task added successfully! ID: {task.id}")
        else:
            print("Error: Failed to add task.")

    def handle_view_tasks(self):
        """Handle viewing all tasks."""
        print("\n--- View All Tasks ---")
        tasks = self.list_tasks()

        if not tasks:
            print("Your task list is empty.")
            return

        print(f"You have {len(tasks)} task(s):")
        for task in sorted(tasks, key=lambda t: t.id):
            print(f"  {task}")

    def handle_update_task(self):
        """Handle updating a task."""
        print("\n--- Update Task ---")
        if not self.tasks:
            print("Your task list is empty. Nothing to update.")
            return

        try:
            task_id = int(input("Enter task ID to update: "))
        except ValueError:
            print("Error: Please enter a valid numeric task ID.")
            return

        task = self.get_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} does not exist.")
            return

        print(f"Current task: {task}")
        new_description = input("Enter new description: ").strip()

        if not new_description:
            print("Error: Task description cannot be empty.")
            return

        if self.update_task(task_id, new_description):
            print(f"Task {task_id} updated successfully!")
        else:
            print("Error: Failed to update task.")

    def handle_delete_task(self):
        """Handle deleting a task."""
        print("\n--- Delete Task ---")
        if not self.tasks:
            print("Your task list is empty. Nothing to delete.")
            return

        try:
            task_id = int(input("Enter task ID to delete: "))
        except ValueError:
            print("Error: Please enter a valid numeric task ID.")
            return

        task = self.get_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} does not exist.")
            return

        print(f"About to delete: {task}")
        confirmation = input("Are you sure you want to delete this task? (y/N): ").strip().lower()

        if confirmation in ['y', 'yes']:
            if self.delete_task(task_id):
                print(f"Task {task_id} deleted successfully!")
            else:
                print("Error: Failed to delete task.")
        else:
            print("Task deletion cancelled.")

    def handle_mark_complete(self):
        """Handle marking a task as complete."""
        print("\n--- Mark Task Complete ---")
        if not self.tasks:
            print("Your task list is empty. Nothing to mark.")
            return

        try:
            task_id = int(input("Enter task ID to mark complete: "))
        except ValueError:
            print("Error: Please enter a valid numeric task ID.")
            return

        task = self.get_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} does not exist.")
            return

        if self.mark_task_complete(task_id):
            print(f"Task {task_id} marked as complete!")
        else:
            print("Error: Failed to mark task as complete.")

    def handle_mark_incomplete(self):
        """Handle marking a task as incomplete."""
        print("\n--- Mark Task Incomplete ---")
        if not self.tasks:
            print("Your task list is empty. Nothing to mark.")
            return

        try:
            task_id = int(input("Enter task ID to mark incomplete: "))
        except ValueError:
            print("Error: Please enter a valid numeric task ID.")
            return

        task = self.get_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} does not exist.")
            return

        if self.mark_task_incomplete(task_id):
            print(f"Task {task_id} marked as incomplete!")
        else:
            print("Error: Failed to mark task as incomplete.")

    def handle_exit(self):
        """Handle application exit."""
        print("\nThank you for using the Todo Application. Goodbye!")


if __name__ == "__main__":
    app = TodoApp()
    app.run()