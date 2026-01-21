# Todo Web App Backend

This is the backend for the Todo Web App, built with FastAPI and Python 3.13. It provides a RESTful API for managing user tasks and authentication.

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Security](#security)
- [Deployment](#deployment)

## Project Structure

```
backend/
├── pyproject.toml                 # Project dependencies and configuration
├── requirements.txt               # Python dependencies
├── todo_app.db                   # SQLite database file
├── src/                          # Source code
│   ├── __init__.py               # Package initialization
│   ├── main.py                   # Application entry point
│   ├── config.py                 # Configuration settings
│   ├── database/                 # Database related modules
│   │   ├── __init__.py           # Database package init
│   │   └── config.py             # Database configuration
│   ├── api/                      # API endpoints
│   │   ├── __init__.py           # API package init
│   │   ├── auth.py               # Authentication endpoints
│   │   └── tasks.py              # Task management endpoints
│   ├── middleware/               # Custom middleware
│   │   ├── __init__.py           # Middleware package init
│   │   └── auth.py               # Authentication middleware
│   ├── models/                   # Database models
│   │   ├── __init__.py           # Models package init
│   │   ├── user.py               # User model
│   │   └── task.py               # Task model
│   ├── services/                 # Business logic services
│   │   ├── __init__.py           # Services package init
│   │   ├── auth.py               # Authentication services
│   │   └── task_service.py       # Task services
│   └── utils/                    # Utility functions
│       ├── __init__.py           # Utils package init
│       ├── exceptions.py         # Custom exceptions
│       └── logging_config.py     # Logging configuration
└── tests/                        # Test suite
    ├── unit/                     # Unit tests
    │   ├── test_auth_middleware.py
    │   └── test_task_service.py
    ├── integration/              # Integration tests
    │   ├── test_auth.py
    │   └── test_tasks.py
    ├── contract/                 # Contract tests
    │   ├── test_auth.py
    │   └── test_tasks.py
    └── security/                 # Security tests
        ├── test_jwt_enforcement.py
        ├── test_jwt_security.py
        └── test_user_isolation.py
```

## Installation

### Prerequisites
- Python 3.13+
- pip package manager

### Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd Todo-App/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
# Or if using Poetry:
poetry install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
# Using uvicorn directly
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Or using the entry point
python -m src.main
```

## Configuration

The backend uses environment variables for configuration. Key settings include:

- `DATABASE_URL`: Database connection string (default: SQLite)
- `JWT_SECRET_KEY`: Secret key for JWT signing
- `JWT_ALGORITHM`: Algorithm for JWT signing (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `SERVER_HOST`: Server hostname
- `SERVER_PORT`: Server port (default: 8000)
- `DEBUG`: Enable/disable debug mode

## API Endpoints

### Authentication Endpoints

#### POST `/v1/auth/signup`
Register a new user account.
- Request Body: `{"email": "string", "password": "string", "first_name": "string", "last_name": "string"}`
- Response: `{"access_token": "string", "token_type": "bearer", "user": User}`

#### POST `/v1/auth/login`
Authenticate user and get access token.
- Request Body: `{"email": "string", "password": "string"}`
- Response: `{"access_token": "string", "token_type": "bearer", "user": User}`

#### GET `/v1/auth/profile`
Get current user profile (requires authentication).
- Response: `User`

#### POST `/v1/auth/logout`
Log out current user (requires authentication).
- Response: `{"message": "Successfully logged out"}`

### Task Endpoints

#### GET `/v1/tasks`
Get all tasks for the current user.
- Response: `{"tasks": [Task]}`

#### POST `/v1/tasks`
Create a new task.
- Request Body: `{"title": "string", "description": "string", "due_date": "string"}`
- Response: `Task`

#### GET `/v1/tasks/{task_id}`
Get a specific task by ID.
- Response: `Task`

#### PUT `/v1/tasks/{task_id}`
Update a specific task.
- Request Body: `{"title": "string", "description": "string", "due_date": "string"}`
- Response: `Task`

#### DELETE `/v1/tasks/{task_id}`
Delete a specific task.
- Response: Success message

#### PATCH `/v1/tasks/{task_id}/complete`
Toggle task completion status.
- Request Body: `{"completed": boolean}`
- Response: `Task`

#### GET `/health`
Health check endpoint.
- Response: `{"status": "healthy"}`

## Database Schema

### User Table
- `id`: UUID (Primary Key)
- `email`: String (Unique, Indexed)
- `first_name`: String
- `last_name`: String
- `is_active`: Boolean (Default: true)
- `password_hash`: String
- `created_at`: DateTime
- `updated_at`: DateTime

### Task Table
- `id`: UUID (Primary Key)
- `title`: String (Indexed)
- `description`: String (Optional)
- `status`: String (Enum: 'pending', 'completed'; Default: 'pending')
- `user_id`: UUID (Foreign Key to User, CASCADE delete)
- `created_at`: DateTime
- `updated_at`: DateTime
- `due_date`: DateTime (Optional)

## Testing

The backend includes a comprehensive test suite with multiple types of tests:

### Unit Tests
Located in `tests/unit/`
- Test individual functions and classes in isolation
- Test business logic in services
- Test utility functions

### Integration Tests
Located in `tests/integration/`
- Test API endpoints
- Test database interactions
- Test middleware functionality

### Contract Tests
Located in `tests/contract/`
- Test API contracts
- Validate request/response schemas
- Test API compliance with specifications

### Security Tests
Located in `tests/security/`
- Test JWT enforcement
- Test security vulnerabilities
- Test user isolation

### Running Tests

```bash
# Run all tests
pytest

# Run specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/contract/
pytest tests/security/

# Run with coverage
pytest --cov=src

# Run with verbose output
pytest -v
```

## Security

### Authentication
- JWT-based authentication
- Secure password hashing with bcrypt
- Token refresh mechanisms
- Role-based access control

### Authorization
- Per-user resource isolation
- Permission checks for sensitive operations
- Input validation and sanitization

### Protection Measures
- Rate limiting to prevent abuse
- SQL injection prevention via SQLAlchemy
- Cross-site scripting (XSS) protection
- Cross-site request forgery (CSRF) protection
- Secure headers and policies

## Deployment

### Production Deployment

1. Set environment variables for production
2. Configure reverse proxy (nginx/Apache)
3. Set up SSL certificates
4. Configure database for production
5. Use process managers like Gunicorn

### Environment Variables for Production
```
DATABASE_URL=postgresql://user:password@localhost/dbname
JWT_SECRET_KEY=your-super-secret-key
DEBUG=false
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

### Docker Deployment (Optional)
```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## API Documentation

The API automatically generates interactive documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Error Handling

The API returns standardized error responses:
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation errors
- `500 Internal Server Error`: Server errors

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.