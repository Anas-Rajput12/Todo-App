import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from datetime import datetime

from src.main import app
from src.models.user import User
from src.models.task import Task, TaskStatus
from src.database import engine
from src.services.auth import hash_password


@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_session():
    """Create a test database session."""
    with Session(engine) as session:
        yield session


@pytest.fixture
def authenticated_client(client: TestClient, db_session: Session):
    """Create a client with an authenticated user."""
    # Create a test user
    user = User(
        email="testuser@example.com",
        password_hash=hash_password("securepassword123"),
        first_name="Test",
        last_name="User"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Login to get a token
    login_response = client.post("/v1/auth/login", json={
        "email": "testuser@example.com",
        "password": "securepassword123"
    })

    token = login_response.json()["access_token"]

    # Add the token to the client headers
    client.headers.update({"Authorization": f"Bearer {token}"})

    yield client, user

    # Cleanup
    client.headers.pop("Authorization", None)


def test_get_tasks_endpoint_contract(authenticated_client):
    """Test the /tasks GET endpoint contract."""
    client, user = authenticated_client

    # Create some tasks for the user
    task_data = {
        "title": "Test Task 1",
        "description": "This is a test task"
    }
    create_response = client.post("/v1/tasks/", json=task_data)
    assert create_response.status_code in [200, 201]

    # Get tasks
    response = client.get("/v1/tasks/")

    # Verify response structure and status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Verify response contains expected fields
    response_data = response.json()
    assert "tasks" in response_data, "Response should contain 'tasks' key"
    assert isinstance(response_data["tasks"], list), "Tasks should be a list"

    # Verify at least one task exists
    assert len(response_data["tasks"]) >= 1, "Should have at least one task"

    # Verify task structure
    task = response_data["tasks"][0]
    expected_fields = ["id", "title", "description", "status", "user_id", "created_at", "updated_at"]
    for field in expected_fields:
        assert field in task, f"Task should contain '{field}' field"

    # Verify task data types
    assert isinstance(task["id"], str), "Task ID should be a string"
    assert isinstance(task["title"], str), "Task title should be a string"
    assert isinstance(task["description"], str) or task["description"] is None, "Task description should be a string or None"
    assert task["status"] in ["pending", "completed"], "Task status should be 'pending' or 'completed'"
    assert isinstance(task["user_id"], str), "Task user_id should be a string"
    assert isinstance(task["created_at"], str), "Task created_at should be a string (ISO format)"
    assert isinstance(task["updated_at"], str), "Task updated_at should be a string (ISO format)"


def test_create_task_endpoint_contract(authenticated_client):
    """Test the /tasks POST endpoint contract."""
    client, user = authenticated_client

    task_data = {
        "title": "New Test Task",
        "description": "This is a new test task",
        "due_date": "2025-12-31T23:59:59"
    }

    response = client.post("/v1/tasks/", json=task_data)

    # Verify response structure and status code
    assert response.status_code in [200, 201], f"Expected 200 or 201, got {response.status_code}"

    # Verify response contains expected fields
    response_data = response.json()
    expected_fields = ["id", "title", "description", "status", "user_id", "created_at", "updated_at", "due_date"]
    for field in expected_fields:
        assert field in response_data, f"Response should contain '{field}' field"

    # Verify field values match input
    assert response_data["title"] == task_data["title"]
    assert response_data["description"] == task_data["description"]
    assert response_data["status"] == "pending"  # Default status
    assert response_data["user_id"] == str(user.id)  # Should belong to authenticated user
    assert response_data["due_date"] == task_data["due_date"]


def test_get_single_task_endpoint_contract(authenticated_client):
    """Test the /tasks/{taskId} GET endpoint contract."""
    client, user = authenticated_client

    # Create a task first
    task_data = {
        "title": "Single Task Test",
        "description": "Testing single task retrieval"
    }
    create_response = client.post("/v1/tasks/", json=task_data)
    assert create_response.status_code in [200, 201]
    created_task = create_response.json()
    task_id = created_task["id"]

    # Get the specific task
    response = client.get(f"/v1/tasks/{task_id}")

    # Verify response structure and status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Verify response contains expected fields
    response_data = response.json()
    expected_fields = ["id", "title", "description", "status", "user_id", "created_at", "updated_at"]
    for field in expected_fields:
        assert field in response_data, f"Response should contain '{field}' field"

    # Verify field values match created task
    assert response_data["id"] == task_id
    assert response_data["title"] == task_data["title"]
    assert response_data["description"] == task_data["description"]
    assert response_data["status"] == "pending"
    assert response_data["user_id"] == str(user.id)


def test_update_task_endpoint_contract(authenticated_client):
    """Test the /tasks/{taskId} PUT endpoint contract."""
    client, user = authenticated_client

    # Create a task first
    task_data = {
        "title": "Original Task",
        "description": "Original description"
    }
    create_response = client.post("/v1/tasks/", json=task_data)
    assert create_response.status_code in [200, 201]
    created_task = create_response.json()
    task_id = created_task["id"]

    # Update the task
    update_data = {
        "title": "Updated Task",
        "description": "Updated description",
        "status": "completed"
    }
    response = client.put(f"/v1/tasks/{task_id}", json=update_data)

    # Verify response structure and status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Verify response contains expected fields
    response_data = response.json()
    expected_fields = ["id", "title", "description", "status", "user_id", "created_at", "updated_at"]
    for field in expected_fields:
        assert field in response_data, f"Response should contain '{field}' field"

    # Verify field values match update
    assert response_data["id"] == task_id
    assert response_data["title"] == update_data["title"]
    assert response_data["description"] == update_data["description"]
    assert response_data["status"] == update_data["status"]


def test_delete_task_endpoint_contract(authenticated_client):
    """Test the /tasks/{taskId} DELETE endpoint contract."""
    client, user = authenticated_client

    # Create a task first
    task_data = {
        "title": "Task to Delete",
        "description": "This task will be deleted"
    }
    create_response = client.post("/v1/tasks/", json=task_data)
    assert create_response.status_code in [200, 201]
    created_task = create_response.json()
    task_id = created_task["id"]

    # Delete the task
    response = client.delete(f"/v1/tasks/{task_id}")

    # Verify response structure and status code
    assert response.status_code == 204, f"Expected 204, got {response.status_code}"

    # Verify the task is actually deleted
    get_response = client.get(f"/v1/tasks/{task_id}")
    assert get_response.status_code == 404


def test_toggle_task_complete_endpoint_contract(authenticated_client):
    """Test the /tasks/{taskId}/complete PATCH endpoint contract."""
    client, user = authenticated_client

    # Create a task first
    task_data = {
        "title": "Toggle Complete Task",
        "description": "Task to test completion toggle"
    }
    create_response = client.post("/v1/tasks/", json=task_data)
    assert create_response.status_code in [200, 201]
    created_task = create_response.json()
    task_id = created_task["id"]

    # Toggle task completion
    toggle_data = {"completed": True}
    response = client.patch(f"/v1/tasks/{task_id}/complete", json=toggle_data)

    # Verify response structure and status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Verify response contains expected fields
    response_data = response.json()
    expected_fields = ["id", "title", "description", "status", "user_id", "created_at", "updated_at"]
    for field in expected_fields:
        assert field in response_data, f"Response should contain '{field}' field"

    # Verify status is now completed
    assert response_data["status"] == "completed"