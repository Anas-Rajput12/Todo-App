import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

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
def setup_users_and_tasks(db_session: Session):
    """Create two users with tasks for isolation testing."""
    # Create first user
    user1 = User(
        email="user1@example.com",
        password_hash=hash_password("securepassword123"),
        first_name="User",
        last_name="One"
    )
    db_session.add(user1)
    db_session.commit()
    db_session.refresh(user1)

    # Create second user
    user2 = User(
        email="user2@example.com",
        password_hash=hash_password("securepassword456"),
        first_name="User",
        last_name="Two"
    )
    db_session.add(user2)
    db_session.commit()
    db_session.refresh(user2)

    # Create tasks for user1
    task1_user1 = Task(
        title="User1 Task 1",
        description="Task for user 1",
        status=TaskStatus.pending,
        user_id=user1.id
    )
    task2_user1 = Task(
        title="User1 Task 2",
        description="Another task for user 1",
        status=TaskStatus.completed,
        user_id=user1.id
    )
    db_session.add(task1_user1)
    db_session.add(task2_user1)

    # Create tasks for user2
    task1_user2 = Task(
        title="User2 Task 1",
        description="Task for user 2",
        status=TaskStatus.pending,
        user_id=user2.id
    )
    task2_user2 = Task(
        title="User2 Task 2",
        description="Another task for user 2",
        status=TaskStatus.pending,
        user_id=user2.id
    )
    db_session.add(task1_user2)
    db_session.add(task2_user2)

    db_session.commit()

    return user1, user2, task1_user1, task2_user1, task1_user2, task2_user2


def test_user_cannot_access_other_users_tasks(client: TestClient, db_session: Session, setup_users_and_tasks):
    """Test that a user cannot access tasks belonging to another user."""
    user1, user2, task1_user1, task2_user1, task1_user2, task2_user2 = setup_users_and_tasks

    # Login as user1
    login_response = client.post("/v1/auth/login", json={
        "email": "user1@example.com",
        "password": "securepassword123"
    })
    assert login_response.status_code == 200

    token1 = login_response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token1}"})

    # Try to access user2's tasks individually
    response_task1_user2 = client.get(f"/v1/tasks/{task1_user2.id}")
    assert response_task1_user2.status_code == 404  # Should not find the task

    response_task2_user2 = client.get(f"/v1/tasks/{task2_user2.id}")
    assert response_task2_user2.status_code == 404  # Should not find the task

    # Get user1's own tasks to confirm they can access their own tasks
    get_tasks_response = client.get("/v1/tasks/")
    assert get_tasks_response.status_code == 200
    user1_tasks = get_tasks_response.json()["tasks"]
    assert len(user1_tasks) == 2  # Should see only their own tasks
    assert any(task["id"] == str(task1_user1.id) for task in user1_tasks)
    assert any(task["id"] == str(task2_user1.id) for task in user1_tasks)
    assert not any(task["id"] == str(task1_user2.id) for task in user1_tasks)  # Should not see user2's tasks
    assert not any(task["id"] == str(task2_user2.id) for task in user1_tasks)  # Should not see user2's tasks

    # Try to update user2's task
    update_response = client.put(f"/v1/tasks/{task1_user2.id}", json={
        "title": "Attempted update by user1"
    })
    assert update_response.status_code == 404  # Should not be able to update

    # Try to delete user2's task
    delete_response = client.delete(f"/v1/tasks/{task1_user2.id}")
    assert delete_response.status_code == 404  # Should not be able to delete

    # Cleanup headers
    client.headers.pop("Authorization", None)


def test_user_can_access_only_their_own_tasks(client: TestClient, db_session: Session, setup_users_and_tasks):
    """Test that a user can only access their own tasks."""
    user1, user2, task1_user1, task2_user1, task1_user2, task2_user2 = setup_users_and_tasks

    # Login as user2
    login_response = client.post("/v1/auth/login", json={
        "email": "user2@example.com",
        "password": "securepassword456"
    })
    assert login_response.status_code == 200

    token2 = login_response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token2}"})

    # Get user2's tasks
    get_tasks_response = client.get("/v1/tasks/")
    assert get_tasks_response.status_code == 200
    user2_tasks = get_tasks_response.json()["tasks"]
    assert len(user2_tasks) == 2  # Should see only their own tasks
    assert any(task["id"] == str(task1_user2.id) for task in user2_tasks)
    assert any(task["id"] == str(task2_user2.id) for task in user2_tasks)
    assert not any(task["id"] == str(task1_user1.id) for task in user2_tasks)  # Should not see user1's tasks
    assert not any(task["id"] == str(task2_user1.id) for task in user2_tasks)  # Should not see user1's tasks

    # Try to access user1's tasks individually
    response_task1_user1 = client.get(f"/v1/tasks/{task1_user1.id}")
    assert response_task1_user1.status_code == 404  # Should not find the task

    response_task2_user1 = client.get(f"/v1/tasks/{task2_user1.id}")
    assert response_task2_user1.status_code == 404  # Should not find the task

    # Cleanup headers
    client.headers.pop("Authorization", None)


def test_cross_user_task_modification_attempts(client: TestClient, db_session: Session, setup_users_and_tasks):
    """Test that users cannot modify each other's tasks."""
    user1, user2, task1_user1, task2_user1, task1_user2, task2_user2 = setup_users_and_tasks

    # Login as user1
    login_response = client.post("/v1/auth/login", json={
        "email": "user1@example.com",
        "password": "securepassword123"
    })
    assert login_response.status_code == 200

    token1 = login_response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token1}"})

    # Attempt to modify user2's task
    modify_response = client.put(f"/v1/tasks/{task1_user2.id}", json={
        "title": "Modified by user1",
        "description": "This should not work"
    })
    assert modify_response.status_code == 404  # Should not be able to modify

    # Attempt to toggle user2's task completion status
    toggle_response = client.patch(f"/v1/tasks/{task1_user2.id}/complete", json={
        "completed": True
    })
    assert toggle_response.status_code == 404  # Should not be able to toggle

    # Verify user2's task remains unchanged
    # Login as user2 to verify
    client.headers.pop("Authorization", None)
    login_response2 = client.post("/v1/auth/login", json={
        "email": "user2@example.com",
        "password": "securepassword456"
    })
    token2 = login_response2.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token2}"})

    verify_response = client.get(f"/v1/tasks/{task1_user2.id}")
    assert verify_response.status_code == 200
    original_task = verify_response.json()
    assert original_task["title"] != "Modified by user1"  # Title should not have changed

    # Cleanup headers
    client.headers.pop("Authorization", None)


def test_user_isolation_on_task_creation(client: TestClient, db_session: Session, setup_users_and_tasks):
    """Test that users can only create tasks for themselves."""
    user1, user2, task1_user1, task2_user1, task1_user2, task2_user2 = setup_users_and_tasks

    # Login as user1
    login_response = client.post("/v1/auth/login", json={
        "email": "user1@example.com",
        "password": "securepassword123"
    })
    assert login_response.status_code == 200

    token1 = login_response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token1}"})

    # Create a new task as user1
    create_response = client.post("/v1/tasks/", json={
        "title": "New task for user1",
        "description": "This is user1's task"
    })
    assert create_response.status_code in [200, 201]

    new_task = create_response.json()
    assert new_task["user_id"] == str(user1.id)  # Task should belong to user1

    # Verify the task appears in user1's task list
    get_tasks_response = client.get("/v1/tasks/")
    assert get_tasks_response.status_code == 200
    user1_tasks = get_tasks_response.json()["tasks"]
    assert any(task["id"] == new_task["id"] for task in user1_tasks)

    # Cleanup headers
    client.headers.pop("Authorization", None)