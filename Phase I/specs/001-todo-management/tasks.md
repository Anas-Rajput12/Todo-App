---
description: "Task list for Todo Management Console Application implementation"
---

# Tasks: Todo Management Console Application

**Input**: Design documents from `/specs/001-todo-management/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan with src/ directory
- [X] T002 Initialize Python 3.13+ project with basic file structure
- [X] T003 [P] Create empty src/models.py, src/task_manager.py, and src/main.py files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Foundational tasks for the todo application:

- [X] T004 Create Task data class in src/models.py with id, title, description, completed fields
- [X] T005 Implement in-memory task storage using Python list in task_manager.py
- [X] T006 Implement unique ID generation for tasks starting from 1
- [X] T007 Create TaskManager class in src/task_manager.py to handle all task operations
- [X] T008 Implement basic CLI menu structure in src/main.py
- [X] T009 Add error handling utilities for invalid inputs

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Allow users to create new tasks with title and optional description

**Independent Test**: Can be fully tested by adding a task with a title and verifying that it appears in the system with a unique ID and proper status.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T010 [P] [US1] Unit test for Task model creation in tests/unit/test_models.py
- [ ] T011 [P] [US1] Unit test for add_task functionality in tests/unit/test_task_manager.py

### Implementation for User Story 1

- [ ] T012 [US1] Implement add_task method in TaskManager class in src/task_manager.py
- [ ] T013 [US1] Add validation to ensure title is not empty in src/task_manager.py
- [ ] T014 [US1] Implement CLI menu option for adding tasks in src/main.py
- [ ] T015 [US1] Add confirmation message with task ID when task is added in src/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P2)

**Goal**: Allow users to see all their tasks with their current status

**Independent Test**: Can be fully tested by adding tasks and then viewing the complete list to verify all tasks are displayed correctly with their status.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US2] Unit test for list_tasks functionality in tests/unit/test_task_manager.py

### Implementation for User Story 2

- [ ] T017 [US2] Implement list_tasks method in TaskManager class in src/task_manager.py
- [ ] T018 [US2] Format task display with ID, title, and completion status in src/main.py
- [ ] T019 [US2] Implement CLI menu option for viewing tasks in src/main.py
- [ ] T020 [US2] Handle case when no tasks exist in src/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task (Priority: P3)

**Goal**: Allow users to modify an existing task's title or description

**Independent Test**: Can be fully tested by creating a task, updating its information, and verifying the changes are reflected when viewing tasks.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T021 [P] [US3] Unit test for update_task functionality in tests/unit/test_task_manager.py

### Implementation for User Story 3

- [ ] T022 [US3] Implement update_task method in TaskManager class in src/task_manager.py
- [ ] T023 [US3] Add validation for task ID existence in src/task_manager.py
- [ ] T024 [US3] Implement CLI menu option for updating tasks in src/main.py
- [ ] T025 [US3] Add confirmation message when task is updated in src/main.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Task (Priority: P4)

**Goal**: Allow users to remove completed or unwanted tasks from their todo list

**Independent Test**: Can be fully tested by creating tasks, deleting one, and verifying it no longer appears in the task list.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T026 [P] [US4] Unit test for delete_task functionality in tests/unit/test_task_manager.py

### Implementation for User Story 4

- [ ] T027 [US4] Implement delete_task method in TaskManager class in src/task_manager.py
- [ ] T028 [US4] Add validation for task ID existence in src/task_manager.py
- [ ] T029 [US4] Implement CLI menu option for deleting tasks in src/main.py
- [ ] T030 [US4] Add confirmation message when task is deleted in src/main.py

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Mark Task Status (Priority: P5)

**Goal**: Allow users to indicate whether a task is completed or pending

**Independent Test**: Can be fully tested by creating tasks, marking them as complete or incomplete, and verifying the status changes are reflected when viewing tasks.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T031 [P] [US5] Unit test for toggle_task_status functionality in tests/unit/test_task_manager.py

### Implementation for User Story 5

- [ ] T032 [US5] Implement toggle_task_status method in TaskManager class in src/task_manager.py
- [ ] T033 [US5] Add validation for task ID existence in src/task_manager.py
- [ ] T034 [US5] Implement CLI menu option for toggling task status in src/main.py
- [ ] T035 [US5] Add confirmation message when task status is changed in src/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T036 [P] Add graceful exit functionality to CLI menu in src/main.py
- [ ] T037 [P] Add input validation for all user inputs in src/main.py
- [ ] T038 [P] Add comprehensive error handling for all operations in src/task_manager.py
- [ ] T039 [P] Add proper formatting for task display in src/main.py
- [ ] T040 [P] Add integration tests for CLI flow in tests/integration/test_cli_flow.py
- [ ] T041 [P] Add docstrings and comments to all functions and classes
- [ ] T042 [P] Run quickstart.md validation to ensure all functionality works as expected

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in priority order (P1 → P2 → P3 → P4 → P5)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in priority order
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in priority order (not truly parallel due to shared resources)

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
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Sequential Team Strategy

With a single developer or when parallel work isn't possible:

1. Team completes Setup + Foundational first
2. Then: User Story 1 (P1) → User Story 2 (P2) → User Story 3 (P3) → User Story 4 (P4) → User Story 5 (P5)
3. Stories complete and integrate independently

---