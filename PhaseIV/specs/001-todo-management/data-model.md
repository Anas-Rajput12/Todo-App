# Data Model: Todo Management Console Application

## Task Entity

### Fields
- **id**: Integer (required, unique, auto-generated)
  - Represents the unique identifier for each task
  - Generated as an incremental integer starting from 1
  - Used for all operations that target a specific task

- **title**: String (required)
  - Represents the task title/description
  - Cannot be empty or null
  - Maximum length: 255 characters

- **description**: String (optional)
  - Provides additional details about the task
  - Can be empty or null
  - Maximum length: 1000 characters

- **completed**: Boolean (required)
  - Represents the completion status of the task
  - Default value: False (pending)
  - Can be toggled between True (completed) and False (pending)

### Validation Rules
- Title must not be empty or contain only whitespace
- ID must be a positive integer
- Completed status must be a boolean value (True/False)

### State Transitions
- A task can transition from "pending" (completed=False) to "completed" (completed=True)
- A task can transition from "completed" (completed=True) to "pending" (completed=False)
- All other fields remain constant during state transitions

## Relationships
- No relationships needed as this is a single-entity system

## Constraints
- All tasks are stored in-memory only during application runtime
- Task IDs are unique within the current application session
- No duplicate task titles are enforced (multiple tasks can have the same title)
- Task IDs are not reused after deletion within the same session