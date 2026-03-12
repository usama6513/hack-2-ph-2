# Tasks: Phase II - Full-Stack Web Todo Application

**Input**: Design documents from `/specs/2-web-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in backend/src/ and frontend/src/
- [X] T002 Initialize backend with Python 3.11, FastAPI, SQLModel dependencies in backend/requirements.txt
- [X] T003 Initialize frontend with Next.js dependencies in frontend/package.json
- [X] T004 [P] Configure linting and formatting tools for both backend and frontend
- [X] T005 [P] Set up initial repository structure with backend/ frontend/ directories

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Setup database schema and migrations framework with Neon PostgreSQL in backend/src/database/init.py
- [X] T007 [P] Implement authentication/authorization framework with Better Auth in backend/src/api/auth.py
- [X] T008 [P] Setup API routing and middleware structure in backend/src/main.py
- [X] T009 Create base User model in backend/src/models/user.py
- [X] T010 Create base Todo model in backend/src/models/todo.py
- [X] T011 Configure error handling and logging infrastructure in backend/src/main.py
- [X] T012 Setup environment configuration management in backend/.env and frontend/.env.local
- [X] T013 [P] Create docker-compose.yml for local development setup
- [X] T014 Setup frontend authentication state management with React Context in frontend/src/hooks/useAuth.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Sign Up (Priority: P1) 🎯 MVP

**Goal**: As a new user, I want to create an account so that I can access my personal todo list.

**Independent Test**: Can be fully tested by navigating to the signup page, entering valid user details, and successfully creating an account that can be used for sign in.

### Implementation for User Story 1

- [X] T015 [P] [US1] Create UserService in backend/src/services/user_service.py
- [X] T016 [US1] Implement user signup endpoint in backend/src/api/auth.py
- [X] T017 [US1] Add user signup validation and error handling in backend/src/api/auth.py
- [X] T018 [US1] Create signup page UI in frontend/src/pages/signup.tsx
- [X] T019 [US1] Create AuthForm component for signup in frontend/src/components/AuthForm.tsx
- [X] T020 [US1] Implement signup form validation in frontend/src/components/AuthForm.tsx
- [X] T021 [US1] Connect frontend signup form to backend API in frontend/src/services/api.ts

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User Sign In (Priority: P1)

**Goal**: As an existing user, I want to sign in so that I can access my personal todo list.

**Independent Test**: Can be fully tested by navigating to the sign in page, entering valid login credentials, and successfully accessing the todo list page.

### Implementation for User Story 2

- [X] T022 [US2] Implement user sign in endpoint in backend/src/api/auth.py
- [X] T023 [US2] Add user sign in validation and error handling in backend/src/api/auth.py
- [X] T024 [US2] Create signin page UI in frontend/src/pages/signin.tsx
- [X] T025 [US2] Update AuthForm component for sign in in frontend/src/components/AuthForm.tsx
- [X] T026 [US2] Implement sign in form validation in frontend/src/components/AuthForm.tsx
- [X] T027 [US2] Connect frontend sign in form to backend API in frontend/src/services/api.ts
- [X] T028 [US2] Implement auth state handling and token storage in frontend/src/hooks/useAuth.ts
- [X] T029 [US2] Redirect to todo list after successful sign in in frontend/src/pages/signin.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Create Todo (Priority: P1)

**Goal**: As an authenticated user, I want to create new todos so that I can track tasks I need to complete.

**Independent Test**: Can be fully tested by signing in, navigating to the create todo form, entering a task description, and successfully saving it to the user's list.

### Implementation for User Story 3

- [X] T030 [P] [US3] Create TodoService in backend/src/services/todo_service.py
- [X] T031 [US3] Implement create todo endpoint in backend/src/api/todos.py
- [X] T032 [US3] Add user-scoped data access enforcement in backend/src/api/todos.py
- [X] T033 [US3] Add todo creation validation and error handling in backend/src/api/todos.py
- [X] T034 [US3] Create TodoForm component in frontend/src/components/TodoForm.tsx
- [X] T035 [US3] Create todo list page UI in frontend/src/pages/todos/index.tsx
- [X] T036 [US3] Connect frontend todo creation to backend API in frontend/src/services/api.ts
- [X] T037 [US3] Add auth middleware to protect todo routes in backend/src/api/todos.py
- [X] T038 [US3] Implement user isolation in TodoService in backend/src/services/todo_service.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - View Todos (Priority: P1)

**Goal**: As an authenticated user, I want to view all my todos so that I can see what tasks I need to complete.

**Independent Test**: Can be fully tested by signing in and viewing the current list of todos associated with the user account.

### Implementation for User Story 4

- [X] T039 [US4] Implement retrieve todos endpoint in backend/src/api/todos.py
- [X] T040 [US4] Add user-scoped data access enforcement for retrieval in backend/src/api/todos.py
- [X] T041 [US4] Add pagination support for todos retrieval in backend/src/api/todos.py
- [X] T042 [P] [US4] Create TodoList component in frontend/src/components/TodoList.tsx
- [X] T043 [US4] Implement todo list display in frontend/src/pages/todos/index.tsx
- [X] T044 [US4] Connect frontend todo retrieval to backend API in frontend/src/services/api.ts
- [X] T045 [US4] Handle empty state for todo list in frontend/src/components/TodoList.tsx
- [X] T046 [US4] Add loading states for todo list in frontend/src/components/TodoList.tsx

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Update Todo (Priority: P2)

**Goal**: As an authenticated user, I want to update my todos so that I can correct descriptions or modify task details.

**Independent Test**: Can be fully tested by signing in, selecting a todo, modifying its description, and saving the changes.

### Implementation for User Story 5

- [X] T047 [US5] Implement update todo endpoint in backend/src/api/todos.py
- [X] T048 [US5] Add user-scoped data access enforcement for update in backend/src/api/todos.py
- [X] T049 [US5] Add todo update validation and error handling in backend/src/api/todos.py
- [X] T050 [US5] Extend TodoForm component for editing in frontend/src/components/TodoForm.tsx
- [X] T051 [US5] Implement todo edit functionality in frontend/src/pages/todos/[id].tsx
- [X] T052 [US5] Connect frontend todo update to backend API in frontend/src/services/api.ts

**Checkpoint**: At this point, User Stories 1-5 should all work independently

---

## Phase 8: User Story 6 - Delete Todo (Priority: P2)

**Goal**: As an authenticated user, I want to delete todos I no longer need so that my list remains manageable and relevant.

**Independent Test**: Can be fully tested by signing in, selecting a todo, and successfully removing it from the list.

### Implementation for User Story 6

- [X] T053 [US6] Implement delete todo endpoint in backend/src/api/todos.py
- [X] T054 [US6] Add user-scoped data access enforcement for deletion in backend/src/api/todos.py
- [X] T055 [US6] Add todo deletion validation and error handling in backend/src/api/todos.py
- [X] T056 [US6] Implement delete todo button in frontend/src/components/TodoList.tsx
- [X] T057 [US6] Add confirmation dialog for todo deletion in frontend/src/components/TodoList.tsx
- [X] T058 [US6] Connect frontend todo deletion to backend API in frontend/src/services/api.ts

**Checkpoint**: At this point, User Stories 1-6 should all work independently

---

## Phase 9: User Story 7 - Toggle Complete/Incomplete (Priority: P2)

**Goal**: As an authenticated user, I want to mark todos as complete or incomplete so that I can track my progress.

**Independent Test**: Can be fully tested by signing in, selecting a todo, and successfully toggling its completion status.

### Implementation for User Story 7

- [X] T059 [US7] Implement toggle todo status endpoint in backend/src/api/todos.py
- [X] T060 [US7] Add user-scoped data access enforcement for status update in backend/src/api/todos.py
- [X] T061 [US7] Add todo status toggle validation and error handling in backend/src/api/todos.py
- [X] T062 [US7] Implement toggle status checkbox in frontend/src/components/TodoList.tsx
- [X] T063 [US7] Connect frontend todo status toggle to backend API in frontend/src/services/api.ts

**Checkpoint**: At this point, User Stories 1-7 should all work independently

---

## Phase 10: User Story 8 - Responsive UI Experience (Priority: P3)

**Goal**: As a user on any device, I want to have a good experience using the application on both desktop and mobile so that I can access my todos anywhere.

**Independent Test**: Can be fully tested by accessing the application on different screen sizes and verifying that the UI adapts appropriately.

### Implementation for User Story 8

- [X] T064 [US8] Implement responsive layout using Tailwind CSS in frontend/src/components/Layout.tsx
- [X] T065 [US8] Add responsive styles to signup/signin pages in frontend/src/pages/
- [X] T066 [US8] Add responsive styles to todo list page in frontend/src/pages/todos/index.tsx
- [X] T067 [US8] Add responsive styles to todo form in frontend/src/components/TodoForm.tsx
- [X] T068 [US8] Add responsive styles to todo list component in frontend/src/components/TodoList.tsx

**Checkpoint**: All user stories should now be independently functional

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T069 [P] Add comprehensive error handling and user feedback throughout frontend
- [X] T070 Add comprehensive error handling and logging throughout backend
- [X] T071 [P] Implement frontend loading states and error boundaries for all API calls
- [X] T072 Add backend validation for all API endpoints with proper error responses
- [X] T073 [P] Add frontend form validation and user-friendly error messages
- [X] T074 Add frontend authentication guards for protected routes
- [X] T075 [P] Implement backend rate limiting and security measures
- [X] T076 Add comprehensive API documentation with examples
- [X] T077 [P] Add README.md with setup and usage instructions
- [X] T078 Run quickstart validation to ensure all functionality works as expected

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1-US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1-US4 but should be independently testable
- **User Story 6 (P6)**: Can start after Foundational (Phase 2) - May integrate with US1-US5 but should be independently testable
- **User Story 7 (P7)**: Can start after Foundational (Phase 2) - May integrate with US1-US6 but should be independently testable
- **User Story 8 (P8)**: Can start after Foundational (Phase 2) - May integrate with US1-US7 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 3

```bash
# Launch all components for User Story 3 together:
Task: "Create TodoService in backend/src/services/todo_service.py"
Task: "Implement create todo endpoint in backend/src/api/todos.py"
Task: "Create TodoForm component in frontend/src/components/TodoForm.tsx"
Task: "Connect frontend todo creation to backend API in frontend/src/services/api.ts"
```

---

## Implementation Strategy

### MVP First (User Stories 1-4 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Sign Up)
4. Complete Phase 4: User Story 2 (Sign In)
5. Complete Phase 5: User Story 3 (Create Todo)
6. Complete Phase 6: User Story 4 (View Todos)
7. **STOP and VALIDATE**: Test User Stories 1-4 independently
8. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1-4 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 5 → Test independently → Deploy/Demo
4. Add User Story 6 → Test independently → Deploy/Demo
5. Add User Story 7 → Test independently → Deploy/Demo
6. Add User Story 8 → Test independently → Deploy/Demo
7. Add Polish → Test independently → Deploy/Demo (Complete!)
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Sign Up)
   - Developer B: User Story 2 (Sign In)
   - Developer C: User Story 3-4 (Create/View Todos)
   - Once these are done:
   - Developer A: User Story 5 (Update Todo)
   - Developer B: User Story 6 (Delete Todo)
   - Developer C: User Story 7 (Toggle Status)
   - Developer D: User Story 8 (Responsive UI)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (if tests are included)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence