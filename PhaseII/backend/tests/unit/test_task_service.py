import pytest
from unittest.mock import Mock, MagicMock
from sqlmodel import Session, select
from datetime import datetime

from src.services.task_service import (
    create_task, get_tasks, get_task, update_task, delete_task, toggle_task_completion
)
from src.models.task import Task, TaskCreate, TaskUpdate, TaskStatus
from src.models.user import User
from src.utils.exceptions import TaskNotFoundException, UnauthorizedAccessException


def test_create_task_success():
    """Test successful task creation."""
    # Arrange
    session = Mock(spec=Session)
    user_id = "some-user-id"

    task_create = TaskCreate(
        title="Test Task",
        description="Test Description",
        due_date=datetime(2025, 12, 31)
    )

    # Mock the session.add, commit, and refresh methods
    session.add = Mock()
    session.commit = Mock()
    session.refresh = Mock()

    # Mock the exec method to return the created task
    created_task = Task(
        id="new-task-id",
        title=task_create.title,
        description=task_create.description,
        status=TaskStatus.pending,
        user_id=user_id,
        due_date=task_create.due_date
    )
    session.refresh.return_value = None  # refresh doesn't return anything

    # Act
    result = create_task(session, task_create, user_id)

    # Assert
    assert result.title == task_create.title
    assert result.description == task_create.description
    assert result.status == TaskStatus.pending
    assert result.user_id == user_id

    # Verify session methods were called
    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()


def test_get_tasks_success():
    """Test successful retrieval of user's tasks."""
    # Arrange
    session = Mock(spec=Session)
    user_id = "some-user-id"

    mock_tasks = [
        Task(id="task1", title="Task 1", description="Desc 1", status=TaskStatus.pending, user_id=user_id),
        Task(id="task2", title="Task 2", description="Desc 2", status=TaskStatus.completed, user_id=user_id)
    ]

    session.exec.return_value.all.return_value = mock_tasks

    # Act
    result = get_tasks(session, user_id)

    # Assert
    assert len(result) == 2
    assert result[0].id == "task1"
    assert result[1].id == "task2"
    assert all(task.user_id == user_id for task in result)


def test_get_task_success():
    """Test successful retrieval of a specific task."""
    # Arrange
    session = Mock(spec=Session)
    task_id = "task-id"
    user_id = "owner-id"

    mock_task = Task(
        id=task_id,
        title="Test Task",
        description="Test Desc",
        status=TaskStatus.pending,
        user_id=user_id
    )

    session.exec.return_value.first.return_value = mock_task

    # Act
    result = get_task(session, task_id, user_id)

    # Assert
    assert result.id == task_id
    assert result.user_id == user_id


def test_get_task_not_found():
    """Test getting a non-existent task raises TaskNotFoundException."""
    # Arrange
    session = Mock(spec=Session)
    task_id = "non-existent-id"
    user_id = "some-user-id"

    session.exec.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(TaskNotFoundException):
        get_task(session, task_id, user_id)


def test_get_task_unauthorized():
    """Test getting a task owned by another user raises UnauthorizedAccessException."""
    # Arrange
    session = Mock(spec=Session)
    task_id = "task-id"
    user_id = "different-user-id"

    mock_task = Task(
        id=task_id,
        title="Test Task",
        description="Test Desc",
        status=TaskStatus.pending,
        user_id="another-owner-id"
    )

    session.exec.return_value.first.return_value = mock_task

    # Act & Assert
    with pytest.raises(UnauthorizedAccessException):
        get_task(session, task_id, user_id)


def test_update_task_success():
    """Test successful task update."""
    # Arrange
    session = Mock(spec=Session)
    task_id = "task-id"
    user_id = "owner-id"

    existing_task = Task(
        id=task_id,
        title="Old Title",
        description="Old Desc",
        status=TaskStatus.pending,
        user_id=user_id
    )

    task_update = TaskUpdate(title="New Title", description="New Desc")

    session.exec.return_value.first.return_value = existing_task

    # Act
    result = update_task(session, task_id, task_update, user_id)

    # Assert
    assert result.title == "New Title"
    assert result.description == "New Desc"
    session.commit.assert_called_once()


def test_update_task_not_found():
    """Test updating a non-existent task raises TaskNotFoundException."""
    # Arrange
    session = Mock(spec=Session)
    task_id = "non-existent-id"
    user_id = "some-user-id"

    task_update = TaskUpdate(title="New Title")

    session.exec.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(TaskNotFoundException):
        update_task(session, task_id, task_update, user_id)


def test_update_task_unauthorized():
    """Test updating a task owned by another user raises UnauthorizedAccessException."""
    # Arrange
    session = Mock(spec=Session)
    task_id = "task-id"
    user_id = "different-user-id"

    task_update = TaskUpdate(title="New Title")

    existing_task = Task(
        id=task_id,
        title="Old Title",
        description="Old Desc",
        status=TaskStatus.pending,
        user_id="another-owner-id"
    )

    session.exec.return_value.first.return_value = existing_task

    # Act & Assert
    with pytest.raises(UnauthorizedAccessException):
        update_task(session, task_id, task_update, user_id)


def test_delete_task_success():
    """Test successful task deletion."""
    # Arrange
    session = Mock(spec=Session)
    task_id = "task-id"
    user_id = "owner-id"

    existing_task = Task(
        id=task_id,
        title="Task to Delete",
        description="Desc",
        status=TaskStatus.pending,
        user_id=user_id
    )

    session.exec.return_value.first.return_value = existing_task
    session.delete = Mock()

    # Act
    delete_task(session, task_id, user_id)

    # Assert
    session.delete.assert_called_once_with(existing_task)
    session.commit.assert_called_once()


def test_delete_task_not_found():
    """Test deleting a non-existent task raises TaskNotFoundException."""
    # Arrange
    session = Mock(spec=Session)
    task_id = "non-existent-id"
    user_id = "some-user-id"

    session.exec.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(TaskNotFoundException):
        delete_task(session, task_id, user_id)


def test_delete_task_unauthorized():
    """Test deleting a task owned by another user raises UnauthorizedAccessException."""
    # Arrange
    session = Mock(spec=Session)
    task_id = "task-id"
    user_id = "different-user-id"

    existing_task = Task(
        id=task_id,
        title="Task to Delete",
        description="Desc",
        status=TaskStatus.pending,
        user_id="another-owner-id"
    )

    session.exec.return_value.first.return_value = existing_task

    # Act & Assert
    with pytest.raises(UnauthorizedAccessException):
        delete_task(session, task_id, user_id)


def test_toggle_task_completion_success():
    """Test successful task completion toggle."""
    # Arrange
    session = Mock(spec=Session)
    task_id = "task-id"
    user_id = "owner-id"

    existing_task = Task(
        id=task_id,
        title="Task to Toggle",
        description="Desc",
        status=TaskStatus.pending,
        user_id=user_id
    )

    session.exec.return_value.first.return_value = existing_task

    # Act
    result = toggle_task_completion(session, task_id, True, user_id)

    # Assert
    assert result.status == TaskStatus.completed
    session.commit.assert_called_once()


def test_toggle_task_completion_mark_pending():
    """Test successful task pending toggle."""
    # Arrange
    session = Mock(spec=Session)
    task_id = "task-id"
    user_id = "owner-id"

    existing_task = Task(
        id=task_id,
        title="Task to Toggle",
        description="Desc",
        status=TaskStatus.completed,
        user_id=user_id
    )

    session.exec.return_value.first.return_value = existing_task

    # Act
    result = toggle_task_completion(session, task_id, False, user_id)

    # Assert
    assert result.status == TaskStatus.pending


def test_toggle_task_completion_not_found():
    """Test toggling completion of a non-existent task raises TaskNotFoundException."""
    # Arrange
    session = Mock(spec=Session)
    task_id = "non-existent-id"
    user_id = "some-user-id"

    session.exec.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(TaskNotFoundException):
        toggle_task_completion(session, task_id, True, user_id)


def test_toggle_task_completion_unauthorized():
    """Test toggling completion of a task owned by another user raises UnauthorizedAccessException."""
    # Arrange
    session = Mock(spec=Session)
    task_id = "task-id"
    user_id = "different-user-id"

    existing_task = Task(
        id=task_id,
        title="Task to Toggle",
        description="Desc",
        status=TaskStatus.pending,
        user_id="another-owner-id"
    )

    session.exec.return_value.first.return_value = existing_task

    # Act & Assert
    with pytest.raises(UnauthorizedAccessException):
        toggle_task_completion(session, task_id, True, user_id)