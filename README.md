# Todo Application - Phase II

A full-stack web application with user authentication and todo management functionality.

## Features

- User authentication (sign up and sign in)
- Create, read, update, and delete todos
- Mark todos as complete/incomplete
- User-specific data isolation
- Responsive UI for desktop and mobile

## Tech Stack

- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **Backend**: Python, FastAPI, SQLModel
- **Database**: PostgreSQL (Neon Serverless)
- **Authentication**: JWT-based authentication

## Prerequisites

- Node.js 18+
- Python 3.11+
- Docker and Docker Compose
- PostgreSQL database

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
# Edit .env with your PostgreSQL connection details and secret key
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

# Run database migrations (if using Alembic)
# alembic upgrade head
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

## Usage

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
- **Update**: Click on a todo description to edit it
- **Delete**: Use the delete button to remove a todo
- **Toggle Status**: Click the checkbox to mark as complete/incomplete

## API Endpoints

### Authentication
- POST /api/auth/signup - Create new user account
- POST /api/auth/login - Authenticate user

### Todos
- GET /api/todos - Get all user's todos
- POST /api/todos - Create a new todo
- PUT /api/todos/{id} - Update a todo
- PATCH /api/todos/{id}/status - Toggle todo completion status
- DELETE /api/todos/{id} - Delete a todo

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

## Project Structure

```
backend/
├── src/
│   ├── models/
│   │   ├── user.py
│   │   └── todo.py
│   ├── services/
│   │   ├── user_service.py
│   │   └── todo_service.py
│   ├── api/
│   │   ├── auth.py
│   │   └── todos.py
│   ├── database/
│   │   └── init.py
│   └── main.py
frontend/
├── src/
│   ├── pages/
│   ├── components/
│   ├── services/
│   ├── hooks/
│   └── types/
├── public/
├── package.json
└── tsconfig.json
```