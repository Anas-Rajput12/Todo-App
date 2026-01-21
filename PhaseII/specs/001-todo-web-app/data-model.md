# Data Model: Todo Web App

## Entity: User

### Fields
- `id`: UUID (Primary Key) - Unique identifier for the user
- `email`: String (Unique, Indexed) - User's email address for login
- `password_hash`: String - Hashed password for authentication
- `first_name`: String (Optional) - User's first name
- `last_name`: String (Optional) - User's last name
- `created_at`: DateTime - Timestamp when user account was created
- `updated_at`: DateTime - Timestamp when user account was last updated
- `is_active`: Boolean - Whether the user account is active (default: true)

### Relationships
- One-to-Many: User → Tasks (via user_id foreign key)

### Validation Rules
- Email must be a valid email format
- Email must be unique across all users
- Password must meet minimum strength requirements (handled by auth library)
- First and last names cannot exceed 50 characters each

## Entity: Task

### Fields
- `id`: UUID (Primary Key) - Unique identifier for the task
- `title`: String (Indexed) - Title of the task (required)
- `description`: Text (Optional) - Detailed description of the task
- `status`: Enum (pending, completed) - Current status of the task (default: pending)
- `user_id`: UUID (Foreign Key) - Reference to the user who owns this task
- `created_at`: DateTime - Timestamp when task was created
- `updated_at`: DateTime - Timestamp when task was last updated
- `due_date`: DateTime (Optional) - Optional deadline for the task

### Relationships
- Many-to-One: Task → User (via user_id foreign key)

### Validation Rules
- Title must be between 1 and 200 characters
- Description cannot exceed 1000 characters
- Status must be either 'pending' or 'completed'
- User_id must reference an existing, active user
- Due date must be in the future if provided

### State Transitions
- `pending` → `completed`: When user marks task as complete
- `completed` → `pending`: When user unmarks task as complete

## Database Constraints

### Primary Keys
- Both User and Task tables have UUID primary keys for global uniqueness

### Foreign Keys
- Task.user_id references User.id with cascade delete behavior
  - When a user is deleted, all their tasks are also deleted

### Indexes
- User.email: Unique index for fast authentication lookups
- Task.user_id: Index for efficient user-specific task queries
- Task.status: Index for filtering by completion status
- Task.created_at: Index for chronological sorting

### Security Constraints
- Row-level security: Users can only access their own tasks
- All queries must include user_id filter for data isolation

## API Integration Points

### Authentication Data Flow
- User registration: Email and password stored with hashed password
- User login: Email lookup, password verification, JWT generation
- JWT payload: Contains user.id for authorization checks

### Task Operations
- Create Task: Requires user_id from JWT token, validates ownership
- Read Tasks: Filters by user_id from JWT token
- Update Task: Validates user_id matches JWT token
- Delete Task: Validates user_id matches JWT token