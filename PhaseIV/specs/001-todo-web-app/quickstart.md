# Quickstart Guide: Todo Web App

## Prerequisites

- Node.js 18+ (for frontend development)
- Python 3.13+ (for backend development)
- PostgreSQL (or access to Neon PostgreSQL)
- Git
- Package managers: npm/yarn/bun for frontend, pip for backend

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd todo-web-app
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your database credentials and JWT secret
```

Environment variables needed:
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT signing
- `JWT_ALGORITHM`: Algorithm for JWT (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiry time (default: 30)

Run database migrations:

```bash
# If using Alembic for migrations
alembic upgrade head
```

Start the backend server:

```bash
uvicorn src.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend  # From repository root
```

Install dependencies:

```bash
npm install
# or
yarn install
# or
bun install
```

Set up environment variables:

```bash
cp .env.example .env.local
# Edit with your backend API URL
```

Environment variables needed:
- `NEXT_PUBLIC_API_BASE_URL`: Base URL for backend API (e.g., http://localhost:8000/v1)

Start the development server:

```bash
npm run dev
# or
yarn dev
# or
bun dev
```

Frontend will be available at `http://localhost:3000`

## API Contract

The API contract is defined in `specs/001-todo-web-app/contracts/openapi.yaml`.
The backend automatically serves OpenAPI documentation at `/docs` when running in development.

## Development Workflow

1. **Feature Development**: Create feature branches from `main`
2. **Testing**: Run tests before committing
   - Backend: `pytest`
   - Frontend: `npm run test`
3. **Code Style**: Follow linting rules
   - Backend: Use Black and Flake8
   - Frontend: Use ESLint and Prettier
4. **Commit Messages**: Follow conventional commits format

## Key Endpoints

### Authentication
- `POST /v1/auth/signup` - User registration
- `POST /v1/auth/login` - User login

### Tasks
- `GET /v1/tasks` - Get user's tasks
- `POST /v1/tasks` - Create a new task
- `PUT /v1/tasks/{id}` - Update a task
- `DELETE /v1/tasks/{id}` - Delete a task
- `PATCH /v1/tasks/{id}/complete` - Toggle task completion status

## Troubleshooting

### Common Issues

1. **Port Already in Use**: Change ports in the startup commands
2. **Database Connection**: Verify your PostgreSQL connection string
3. **JWT Issues**: Check that the secret key matches between frontend and backend
4. **CORS Errors**: Ensure backend allows requests from frontend origin

### Environment Setup

Make sure all required environment variables are set in both backend and frontend.

## Running Tests

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## Deployment

### Backend Deployment
The backend is designed to work with containerization tools like Docker.

### Frontend Deployment
The Next.js app is configured for deployment on Vercel (as per constitution).

Update environment variables in your deployment platform to point to the production backend API.