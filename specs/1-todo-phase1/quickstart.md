# Quickstart Guide: Phase I - Basic Todo Console Application

**Date**: 2026-02-24
**Feature**: Phase I - Basic Todo Console Application

## Getting Started

1. **Prerequisites**: Python 3.11 or higher installed on your system

2. **Running the Application**:
   ```bash
   python todo_app.py
   ```

3. **Main Menu Options**:
   - Option 1: Add a new task
   - Option 2: View all tasks
   - Option 3: Update a task description
   - Option 4: Delete a task
   - Option 5: Mark a task as complete
   - Option 6: Mark a task as incomplete
   - Option 7: Exit the application

## Basic Usage

### Adding a Task
1. Select option "1" from the main menu
2. Enter your task description when prompted
3. The task will be added with a unique ID and "Incomplete" status

### Viewing Tasks
1. Select option "2" from the main menu
2. All tasks will be displayed with their ID, description, and status

### Updating a Task
1. Select option "3" from the main menu
2. Enter the task ID you want to update
3. Enter the new description for the task

### Deleting a Task
1. Select option "4" from the main menu
2. Enter the task ID you want to delete
3. Confirm the deletion when prompted

### Marking Complete/Incomplete
1. Select option "5" to mark complete or "6" to mark incomplete
2. Enter the task ID you want to update
3. The task status will be updated accordingly

## Error Handling
- If you enter an invalid task ID, the application will display an error message
- If you try to perform operations on an empty task list, you will receive an appropriate message
- Invalid menu options will prompt you to try again

## Exiting
- Select option "7" from the main menu to exit the application gracefully