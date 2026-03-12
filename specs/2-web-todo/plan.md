# Implementation Plan: Phase II - Full-Stack Web Todo Application

**Branch**: `2-web-todo` | **Date**: 2026-02-24 | **Spec**: [specs/2-web-todo/spec.md](specs/2-web-todo/spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a full-stack web application with Next.js frontend and Python/FastAPI backend. The system provides a complete todo management solution with user authentication, secure data isolation, and responsive UI. The architecture maintains clean separation between frontend and backend with secure API communication and proper user data ownership enforcement.

## Technical Context

**Language/Version**: Python 3.11 for backend, JavaScript/TypeScript for frontend
**Primary Dependencies**: FastAPI for backend REST API, Next.js for frontend framework, Better Auth for authentication, SQLModel for data modeling
**Storage**: Neon Serverless PostgreSQL database
**Testing**: pytest for backend tests, Jest/React Testing Library for frontend tests
**Target Platform**: Web application (desktop and mobile browsers)
**Project Type**: Web application with separate frontend/backend
**Performance Goals**: <200ms API response time, <3 second page load times
**Constraints**: <500ms p95 for operations, <100MB memory per service, web-only interface
**Scale/Scope**: Single user authentication, up to 1000 todos per user, individual data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Spec-Driven Development: Plan follows approved spec from specs/2-web-todo/spec.md
- ✅ Agent Behavior Rules: No feature invention, following only approved requirements
- ✅ Phase Governance: Phase II requirements followed (auth, web app, no future features)
- ✅ Technology Constraints: Using Python REST API, Neon PostgreSQL, Next.js, Better Auth as required by constitution
- ✅ Quality Principles: Clean architecture with separation of concerns implemented

## Project Structure

### Documentation (this feature)

```text
specs/2-web-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
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
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── requirements.txt
└── alembic/
    └── versions/

frontend/
├── src/
│   ├── pages/
│   │   ├── index.tsx
│   │   ├── signup.tsx
│   │   ├── signin.tsx
│   │   ├── todos/
│   │   │   ├── index.tsx
│   │   │   └── [id].tsx
│   │   └── _app.tsx
│   ├── components/
│   │   ├── TodoForm.tsx
│   │   ├── TodoList.tsx
│   │   ├── AuthForm.tsx
│   │   └── Layout.tsx
│   ├── services/
│   │   └── api.ts
│   ├── hooks/
│   │   └── useAuth.ts
│   └── types/
│       └── index.ts
├── tests/
├── public/
├── package.json
├── next.config.js
└── tsconfig.json

.env
.env.example
docker-compose.yml
README.md
```

**Structure Decision**: Separate backend/frontend structure with backend in Python/FastAPI and frontend in Next.js. This follows the clean separation requirement from the constitution and allows for independent scaling and development.

## Phase 1: Design & Implementation Approach

### Backend Plan
- **Framework responsibility**: FastAPI will handle REST API routing, request validation, response serialization, and documentation
- **API routing structure**: Separate router files for auth endpoints and todo endpoints, with proper authentication middleware
- **Authentication integration**: Better Auth integrated for user signup/login, with middleware to protect routes and extract user identity
- **Data persistence**: SQLModel with Neon PostgreSQL for defining data models and executing database operations
- **User-to-do ownership**: Foreign key relationship between User and Todo models, with query filtering to ensure users only access their own data
- **Error handling approach**: Custom exception handlers with appropriate HTTP status codes, request validation errors automatically handled by FastAPI

### Frontend Plan
- **Next.js application structure**: Page router with dedicated pages for auth flows and todo operations
- **Page-level routing**: Separate Next.js pages for signup, signin, todos dashboard, and todo edit views
- **Component responsibilities**: Reusable components for todo forms, lists, and auth forms with clear separation of concerns
- **API communication strategy**: Custom API service module to handle all backend communication with proper error handling
- **Authentication state handling**: React context API for global auth state management with hooks for easy access
- **Responsive UI strategy**: Tailwind CSS for responsive design with mobile-first approach and responsive breakpoints

### Database Plan
- **User data model**: SQLModel with fields for id, email, hashed password, timestamps, and todo relationship
- **Todo data model**: SQLModel with fields for id, description, completed status, user_id foreign key, timestamps
- **Relationship**: One-to-many relationship from User to Todo with proper foreign key constraints
- **Migration approach**: Alembic for database schema migrations with initial setup and future change management

### Integration Plan
- **Frontend ↔ Backend communication**: REST API calls with JSON payloads, proper error handling and loading states
- **Auth token/session flow**: Better Auth tokens passed in request headers for API authentication
- **Local development setup**: Docker Compose for local development with separate services for frontend, backend, and PostgreSQL