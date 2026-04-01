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
        email="task_test_user@example.com",
        password_hash=hash_password("securepassword123"),
        first_name="Task",
        last_name="Tester"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Login to get a token
    login_response = client.post("/v1/auth/login", json={
        "email": "task_test_user@example.com",
        "password": "securepassword123"
    })

    token = login_response.json()["access_token"]

    # Add the token to the client headers
    client.headers.update({"Authorization": f"Bearer {token}"})

    yield client, user

    # Cleanup
    client.headers.pop("Authorization", None)


def test_task_crud_operations_integration(authenticated_client):
    """Test the complete task CRUD operations integration."""
    client, user = authenticated_client

    # CREATE: Create a new task
    task_data = {
        "title": "Integration Test Task",
        "description": "This is a test task for integration testing",
        "due_date": "2025-12-31T23:59:59"
    }

    create_response = client.post("/v1/tasks/", json=task_data)
    assert create_response.status_code in [200, 201]

    created_task = create_response.json()
    task_id = created_task["id"]

    # Verify the created task has correct data
    assert created_task["title"] == task_data["title"]
    assert created_task["description"] == task_data["description"]
    assert created_task["status"] == "pending"
    assert created_task["user_id"] == str(user.id)
    assert created_task["due_date"] == task_data["due_date"]

    # READ: Get the specific task
    get_one_response = client.get(f"/v1/tasks/{task_id}")
    assert get_one_response.status_code == 200

    retrieved_task = get_one_response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["title"] == task_data["title"]
    assert retrieved_task["description"] == task_data["description"]

    # READ: Get all tasks for the user
    get_all_response = client.get("/v1/tasks/")
    assert get_all_response.status_code == 200

    tasks_list = get_all_response.json()["tasks"]
    assert len([t for t in tasks_list if t["id"] == task_id]) == 1

    # UPDATE: Modify the task
    update_data = {
        "title": "Updated Integration Test Task",
        "description": "Updated description for integration testing",
        "status": "completed"
    }

    update_response = client.put(f"/v1/tasks/{task_id}", json=update_data)
    assert update_response.status_code == 200

    updated_task = update_response.json()
    assert updated_task["id"] == task_id
    assert updated_task["title"] == update_data["title"]
    assert updated_task["description"] == update_data["description"]
    assert updated_task["status"] == update_data["status"]

    # Confirm the update by retrieving again
    verify_response = client.get(f"/v1/tasks/{task_id}")
    assert verify_response.status_code == 200
    confirmed_task = verify_response.json()
    assert confirmed_task["title"] == update_data["title"]
    assert confirmed_task["status"] == update_data["status"]

    # DELETE: Remove the task
    delete_response = client.delete(f"/v1/tasks/{task_id}")
    assert delete_response.status_code == 204

    # Verify the task is gone
    not_found_response = client.get(f"/v1/tasks/{task_id}")
    assert not_found_response.status_code == 404


def test_task_completion_toggle_integration(authenticated_client):
    """Test the task completion toggle functionality integration."""
    client, user = authenticated_client

    # Create a task
    task_data = {
        "title": "Completion Toggle Test",
        "description": "Testing the completion toggle functionality"
    }

    create_response = client.post("/v1/tasks/", json=task_data)
    assert create_response.status_code in [200, 201]
    created_task = create_response.json()
    task_id = created_task["id"]

    # Verify initial status is pending
    assert created_task["status"] == "pending"

    # Toggle to completed
    toggle_to_completed = {"completed": True}
    complete_response = client.patch(f"/v1/tasks/{task_id}/complete", json=toggle_to_completed)
    assert complete_response.status_code == 200

    completed_task = complete_response.json()
    assert completed_task["status"] == "completed"

    # Toggle back to pending
    toggle_to_pending = {"completed": False}
    pending_response = client.patch(f"/v1/tasks/{task_id}/complete", json=toggle_to_pending)
    assert pending_response.status_code == 200

    pending_task = pending_response.json()
    assert pending_task["status"] == "pending"


def test_user_task_isolation_integration(authenticated_client, db_session):
    """Test that users can only access their own tasks."""
    client, user = authenticated_client

    # Create a task for the first user
    task_data = {
        "title": "User 1 Task",
        "description": "This belongs to user 1"
    }

    create_response = client.post("/v1/tasks/", json=task_data)
    assert create_response.status_code in [200, 201]
    created_task = create_response.json()
    task_id = created_task["id"]

    # Create a second user
    user2 = User(
        email="other_user@example.com",
        password_hash=hash_password("otherpassword123"),
        first_name="Other",
        last_name="User"
    )
    db_session.add(user2)
    db_session.commit()
    db_session.refresh(user2)

    # Login as second user
    login_response2 = client.post("/v1/auth/login", json={
        "email": "other_user@example.com",
        "password": "otherpassword123"
    })
    assert login_response2.status_code == 200
    token2 = login_response2.json()["access_token"]

    # Update client headers to second user
    client.headers.update({"Authorization": f"Bearer {token2}"})

    # Second user should not be able to access first user's task
    access_response = client.get(f"/v1/tasks/{task_id}")
    assert access_response.status_code in [404, 403]  # Either not found or forbidden

    # Second user should only see their own tasks (which should be none initially)
    get_all_response = client.get("/v1/tasks/")
    assert get_all_response.status_code == 200
    user2_tasks = get_all_response.json()["tasks"]
    assert len(user2_tasks) == 0

    # Cleanup: switch back to first user and delete test users
    client.headers.update({"Authorization": f"Bearer {login_response.json()['access_token']}"})
    db_session.delete(user2)
    db_session.commit()


def test_task_validation_integration(authenticated_client):
    """Test task validation during creation and updates."""
    client, user = authenticated_client

    # Test creating a task without a title (should fail)
    invalid_task_data = {
        "description": "Task without a title should fail"
    }

    create_response = client.post("/v1/tasks/", json=invalid_task_data)
    # This may return 422 (validation error) or 400 (bad request)
    assert create_response.status_code in [422, 400]

    # Test creating a valid task
    valid_task_data = {
        "title": "Valid Test Task",
        "description": "This should work fine"
    }

    create_valid_response = client.post("/v1/tasks/", json=valid_task_data)
    assert create_valid_response.status_code in [200, 201]
    valid_task = create_valid_response.json()

    # Verify the task was created with correct defaults
    assert valid_task["title"] == valid_task_data["title"]
    assert valid_task["status"] == "pending"  # Default status