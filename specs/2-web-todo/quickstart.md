# Quickstart Guide: Phase II - Full-Stack Web Todo Application

**Date**: 2026-02-24
**Feature**: Phase II - Full-Stack Web Todo Application

## Prerequisites

- Node.js 18+ installed
- Python 3.11+ installed
- Docker and Docker Compose (recommended) or direct PostgreSQL access
- Neon Serverless PostgreSQL account and database

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Neon PostgreSQL connection details and Better Auth secrets
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with backend API URL and other configuration
```

### 4. Database Setup
```bash
# From backend directory
cd backend

# Run database migrations
alembic upgrade head
```

### 5. Running the Application

#### Option A: Using Docker Compose (Recommended)
```bash
# From project root
docker-compose up --build
```

#### Option B: Running Separately
```bash
# Terminal 1: Start backend
cd backend
uvicorn src.main:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend
npm run dev
```

## Application Access

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API Documentation: http://localhost:8000/docs

## Basic Usage

### 1. Sign Up
- Navigate to http://localhost:3000/signup
- Enter a valid email and strong password
- Account will be created and you'll be redirected to the todo dashboard

### 2. Sign In
- Navigate to http://localhost:3000/signin
- Enter your registered email and password
- Access your todo list at http://localhost:3000/todos

### 3. Managing Todos
- **Create**: Click "Add Todo" and enter a description
- **View**: See all your todos on the main dashboard
- **Update**: Click on a todo to edit its description
- **Delete**: Use the delete button to remove a todo
- **Toggle Status**: Click the checkbox to mark as complete/incomplete

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## API Endpoints

### Authentication
- POST /api/auth/signup - Create new user account
- POST /api/auth/login - Authenticate user
- POST /api/auth/logout - Log out user

### Todos
- GET /api/todos - Get all user's todos
- POST /api/todos - Create a new todo
- PUT /api/todos/{id} - Update a todo
- PATCH /api/todos/{id}/status - Toggle todo completion status
- DELETE /api/todos/{id} - Delete a todo