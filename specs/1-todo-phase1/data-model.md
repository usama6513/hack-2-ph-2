# Data Model: Phase I - Basic Todo Console Application

**Date**: 2026-02-24
**Feature**: Phase I - Basic Todo Console Application

## Task Entity

**Description**: Represents a single todo item in the application

**Fields**:
- `id` (int): Unique identifier for the task, generated sequentially starting from 1
- `description` (str): Text description of the task, non-empty
- `completed` (bool): Status indicating whether the task is completed (True) or incomplete (False)

**Validation Rules**:
- `id` must be a positive integer
- `description` must be non-empty (length > 0)
- `completed` must be a boolean value (True or False)

**State Transitions**:
- `completed` can transition from False → True (mark as complete)
- `completed` can transition from True → False (mark as incomplete)

## Task Storage Structure

**In-Memory Data Structure**: Dictionary mapping task IDs to Task objects
- Key: `id` (int) - the unique task identifier
- Value: `Task` object containing description and completion status

**ID Generation Strategy**: Sequential integer starting from 1, incrementing with each new task
- Uses the next available integer based on current highest ID in the collection
- Guarantees uniqueness without collisions

## Task List Operations

**Supported Operations**:
- Add: Creates a new Task with a unique ID and "incomplete" status
- Retrieve: Access a Task by its ID
- Update: Modify the description of an existing Task
- Delete: Remove a Task by its ID
- Mark Complete: Update the status of a Task to completed
- Mark Incomplete: Update the status of a Task to incomplete
- List All: Retrieve all Tasks in the collection