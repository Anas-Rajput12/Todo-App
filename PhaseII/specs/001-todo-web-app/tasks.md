---
description: "Task list for Todo Web App implementation"
---

# Tasks: Todo Web App

**Input**: Design documents from `/specs/001-todo-web-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Included as requested in feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend project structure with FastAPI dependencies in backend/
- [x] T002 Create frontend project structure with Next.js 16 dependencies in frontend/
- [x] T003 [P] Initialize backend requirements.txt with FastAPI, SQLModel, Neon DB dependencies
- [x] T004 [P] Initialize frontend package.json with Next.js 16, TypeScript, Tailwind CSS dependencies
- [x] T005 [P] Configure linting and formatting tools for both backend and frontend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Setup Neon PostgreSQL database connection with SQLModel in backend/src/database/
- [x] T007 [P] Implement JWT authentication framework in backend/src/middleware/auth.py
- [x] T008 [P] Setup API routing and middleware structure in backend/src/main.py
- [x] T009 Create base User and Task models in backend/src/models/ (depends on T006)
- [x] T010 Configure error handling and logging infrastructure in backend/src/utils/
- [x] T011 Setup environment configuration management in backend/src/config/
- [x] T012 Create shared types for User and Task in shared/types/
- [x] T013 Setup API client in frontend/src/lib/api-client.ts
- [x] T014 Implement auth utilities in frontend/src/lib/auth.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable new users to sign up and existing users to log in securely to access their personal todo lists

**Independent Test**: Can be fully tested by creating an account, logging in, and verifying that the system recognizes the user's identity. Delivers the core value of personalized todo management.

### Tests for User Story 1 (INCLUDED - as requested in feature spec) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T015 [P] [US1] Contract test for /auth/signup endpoint in backend/tests/contract/test_auth.py
- [x] T016 [P] [US1] Contract test for /auth/login endpoint in backend/tests/contract/test_auth.py
- [x] T017 [P] [US1] Integration test for user registration flow in backend/tests/integration/test_auth.py
- [x] T018 [P] [US1] Integration test for user login flow in backend/tests/integration/test_auth.py
- [x] T019 [P] [US1] Unit test for JWT middleware in backend/tests/unit/test_auth_middleware.py

### Implementation for User Story 1

- [x] T020 [P] [US1] Create User model with all fields and validation in backend/src/models/user.py (depends on T009)
- [x] T021 [US1] Implement authentication service with signup/login logic in backend/src/services/auth.py (depends on T020)
- [x] T022 [US1] Implement /auth/signup and /auth/login endpoints in backend/src/api/auth.py (depends on T021, T007)
- [x] T023 [US1] Add validation and error handling for authentication endpoints
- [x] T024 [P] [US1] Create login page component in frontend/src/app/login/page.tsx
- [x] T025 [P] [US1] Create signup page component in frontend/src/app/signup/page.tsx
- [x] T026 [US1] Implement authentication forms with validation in frontend/src/components/auth/
- [x] T027 [US1] Add auth context/provider for state management in frontend/src/contexts/auth.tsx
- [x] T028 [US1] Add logging for authentication operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management (Priority: P1)

**Goal**: Allow authenticated users to create, view, update, delete, and mark tasks as complete with clear status indicators

**Independent Test**: Can be fully tested by performing all CRUD operations on tasks and verifying they persist correctly. Delivers the essential todo management functionality.

### Tests for User Story 2 (INCLUDED - as requested in feature spec) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T029 [P] [US2] Contract test for /tasks GET endpoint in backend/tests/contract/test_tasks.py
- [x] T030 [P] [US2] Contract test for /tasks POST endpoint in backend/tests/contract/test_tasks.py
- [x] T031 [P] [US2] Contract test for /tasks/{taskId} PUT endpoint in backend/tests/contract/test_tasks.py
- [x] T032 [P] [US2] Contract test for /tasks/{taskId} DELETE endpoint in backend/tests/contract/test_tasks.py
- [x] T033 [P] [US2] Contract test for /tasks/{taskId}/complete PATCH endpoint in backend/tests/contract/test_tasks.py
- [x] T034 [P] [US2] Integration test for task CRUD operations in backend/tests/integration/test_tasks.py
- [x] T035 [P] [US2] Unit test for task service functions in backend/tests/unit/test_task_service.py

### Implementation for User Story 2

- [x] T036 [P] [US2] Enhance Task model with all fields and validation in backend/src/models/task.py (depends on T009)
- [x] T037 [US2] Implement task service with CRUD operations in backend/src/services/task_service.py (depends on T036, T020)
- [x] T038 [US2] Implement all task endpoints (/tasks GET/POST, /tasks/{id} GET/PUT/DELETE, /tasks/{id}/complete PATCH) in backend/src/api/tasks.py (depends on T037, T007)
- [x] T039 [US2] Add JWT validation and user isolation to task endpoints (depends on T007)
- [x] T040 [US2] Add validation and error handling for task operations
- [x] T041 [P] [US2] Create task list component in frontend/src/components/tasks/task-list.tsx
- [x] T042 [P] [US2] Create task item component with status indicators in frontend/src/components/tasks/task-item.tsx
- [x] T043 [P] [US2] Create task form component in frontend/src/components/tasks/task-form.tsx
- [x] T044 [US2] Implement dashboard page with task management in frontend/src/app/dashboard/page.tsx
- [x] T045 [US2] Connect frontend components to backend API for task operations
- [x] T046 [US2] Add status badge UI with visual indicators for completed/pending tasks

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Responsive UI Experience (Priority: P2)

**Goal**: Enable users to access and interact with their todo lists seamlessly across different devices with appropriate loading and empty states

**Independent Test**: Can be fully tested by accessing the application on different screen sizes and verifying responsive behavior. Delivers consistent experience across all user contexts.

### Tests for User Story 3 (INCLUDED - as requested in feature spec) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T047 [P] [US3] UI responsiveness test for mobile viewport in frontend/tests/e2e/test_responsive_ui.ts
- [ ] T048 [P] [US3] UI responsiveness test for tablet viewport in frontend/tests/e2e/test_responsive_ui.ts
- [ ] T049 [P] [US3] Empty state test in frontend/tests/integration/test_empty_states.ts
- [ ] T050 [P] [US3] Loading state test in frontend/tests/integration/test_loading_states.ts

### Implementation for User Story 3

- [x] T051 [P] [US3] Create responsive layout components in frontend/src/components/ui/layout.tsx
- [x] T052 [P] [US3] Implement mobile-optimized navigation in frontend/src/components/ui/navigation.tsx
- [x] T053 [US3] Add responsive design to task components using Tailwind CSS
- [x] T054 [US3] Implement empty state UI for task list in frontend/src/components/tasks/empty-state.tsx
- [x] T055 [US3] Implement loading states for task operations in frontend/src/components/ui/loading.tsx
- [x] T056 [US3] Add button hover animations and visual feedback in frontend/src/components/ui/buttons.tsx
- [x] T057 [US3] Optimize all components for mobile viewport (320px-768px)
- [x] T058 [US3] Add media queries and responsive breakpoints in frontend/src/app/globals.css

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Quality Assurance & Security

**Goal**: Ensure all security requirements are met and user isolation is enforced

### QA Tests (INCLUDED - as requested in feature spec) ⚠️

- [x] T059 [P] [QA] JWT enforcement test - verify unauthorized access is blocked in backend/tests/security/test_jwt_enforcement.py
- [x] T060 [P] [QA] User isolation test - verify users can't access other users' tasks in backend/tests/security/test_user_isolation.py
- [x] T061 [P] [QA] Session management test in backend/tests/security/test_jwt_security.py
- [x] T062 [P] [QA] UI security test - verify sensitive data is not exposed in frontend/tests/security/test_ui_security.ts

### Implementation for Security

- [x] T063 [QA] Add comprehensive input validation and sanitization across all endpoints
- [x] T064 [QA] Implement rate limiting for authentication endpoints
- [x] T065 [QA] Add security headers to FastAPI application
- [x] T066 [QA] Implement proper password hashing in User model
- [ ] T067 [QA] Add CSRF protection for authentication flows

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T068 [P] Documentation updates in docs/
- [ ] T069 Code cleanup and refactoring
- [ ] T070 Performance optimization across all stories
- [ ] T071 [P] Additional unit tests (if requested) in backend/tests/unit/ and frontend/tests/
- [ ] T072 Security hardening
- [ ] T073 Run quickstart.md validation
- [ ] T074 Add comprehensive error handling and user-friendly error messages
- [ ] T075 Optimize database queries and add proper indexing
- [ ] T076 Add proper logging throughout the application

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 authentication for user isolation
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 and US2 for UI components
- **QA Phase**: Depends on all user stories being implemented

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together:
Task: "Contract test for /tasks GET endpoint in backend/tests/contract/test_tasks.py"
Task: "Contract test for /tasks POST endpoint in backend/tests/contract/test_tasks.py"
Task: "Integration test for task CRUD operations in backend/tests/integration/test_tasks.py"

# Launch all models for User Story 2 together:
Task: "Enhance Task model with all fields and validation in backend/src/models/task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add QA Phase → Test security requirements → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: QA & Security
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence