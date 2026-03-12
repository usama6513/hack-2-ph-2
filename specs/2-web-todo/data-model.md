# Data Model: Phase II - Full-Stack Web Todo Application

**Date**: 2026-02-24
**Feature**: Phase II - Full-Stack Web Todo Application

## User Entity

**Description**: Represents an authenticated user in the system

**Fields**:
- `id` (int/UUID): Unique identifier for the user, auto-generated
- `email` (str): User's email address, unique and required
- `hashed_password` (str): Securely hashed password
- `created_at` (datetime): Timestamp of account creation
- `updated_at` (datetime): Timestamp of last update

**Validation Rules**:
- `email` must be a valid email format
- `email` must be unique across all users
- `hashed_password` must be present and securely hashed

## Todo Entity

**Description**: Represents a single todo item associated with a user

**Fields**:
- `id` (int): Unique identifier for the todo, auto-generated
- `description` (str): Text description of the task
- `completed` (bool): Status indicating whether the task is completed
- `user_id` (int/UUID): Foreign key reference to the owning user
- `created_at` (datetime): Timestamp of todo creation
- `updated_at` (datetime): Timestamp of last update

**Validation Rules**:
- `description` must be non-empty (length > 0)
- `completed` must be a boolean value (True or False)
- `user_id` must reference an existing user
- `description` has a maximum length to prevent abuse

**State Transitions**:
- `completed` can transition from False → True (mark as complete)
- `completed` can transition from True → False (mark as incomplete)

## Database Schema Relationships

**User to Todo (One-to-Many)**:
- One user can own many todos
- Foreign key: `todos.user_id` references `users.id`
- When a user is deleted, their todos should also be deleted (cascade delete)

## API Request/Response Models

### User Creation Request
- `email` (string, required)
- `password` (string, required with minimum length validation)

### User Response (excluding sensitive data)
- `id` (int/UUID)
- `email` (string)
- `created_at` (datetime)

### Todo Creation Request
- `description` (string, required)
- `completed` (bool, optional, default: false)

### Todo Response
- `id` (int)
- `description` (string)
- `completed` (bool)
- `user_id` (int/UUID)
- `created_at` (datetime)
- `updated_at` (datetime)

### Todo Update Request
- `description` (string, optional)
- `completed` (bool, optional)