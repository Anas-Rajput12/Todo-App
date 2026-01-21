import logging
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from ..models.user import User
from ..models.task import Task, TaskCreate, TaskUpdate, TaskStatus
from ..utils.exceptions import TaskNotFoundException, UnauthorizedAccessException


# Set up logger
logger = logging.getLogger(__name__)


def create_task(session: Session, task_create: TaskCreate, user_id: str) -> Task:
    """
    Create a new task for a user.

    Args:
        session: Database session
        task_create: Task creation data
        user_id: ID of the user creating the task

    Returns:
        Task: The created task
    """
    import uuid

    logger.info(f"Creating task for user ID: {user_id}")

    # Convert the user_id string to UUID
    user_uuid = uuid.UUID(user_id) if not isinstance(user_id, uuid.UUID) else user_id

    task = Task(
        title=task_create.title,
        description=task_create.description,
        status=TaskStatus.pending,  # Default status
        user_id=user_uuid,
        due_date=task_create.due_date
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    logger.info(f"Successfully created task ID: {task.id} for user ID: {user_id}")
    return task


def get_tasks(session: Session, user_id: str) -> List[Task]:
    """
    Get all tasks for a specific user.

    Args:
        session: Database session
        user_id: ID of the user whose tasks to retrieve

    Returns:
        List[Task]: List of tasks belonging to the user
    """
    import uuid

    logger.debug(f"Retrieving tasks for user ID: {user_id}")

    # Convert the user_id string to UUID
    user_uuid = uuid.UUID(user_id) if not isinstance(user_id, uuid.UUID) else user_id

    statement = select(Task).where(Task.user_id == user_uuid)
    tasks = session.exec(statement).all()

    logger.info(f"Retrieved {len(tasks)} tasks for user ID: {user_id}")
    return tasks


def get_task(session: Session, task_id: str, user_id: str) -> Task:
    """
    Get a specific task for a user.

    Args:
        session: Database session
        task_id: ID of the task to retrieve
        user_id: ID of the user who owns the task

    Returns:
        Task: The requested task

    Raises:
        TaskNotFoundException: If the task doesn't exist
        UnauthorizedAccessException: If the user doesn't own the task
    """
    import uuid

    logger.debug(f"Retrieving task ID: {task_id} for user ID: {user_id}")

    try:
        # Convert the user_id string to UUID
        user_uuid = uuid.UUID(user_id) if not isinstance(user_id, uuid.UUID) else user_id

        # Convert the task_id string to UUID for comparison
        task_uuid = uuid.UUID(task_id) if not isinstance(task_id, uuid.UUID) else task_id

        statement = select(Task).where(Task.id == task_uuid)
        task = session.exec(statement).first()

        if not task:
            logger.warning(f"Task with ID {task_id} not found")
            raise TaskNotFoundException(task_id)

        if task.user_id != user_uuid:
            logger.warning(f"User {user_id} attempted to access task {task_id} owned by user {task.user_id}")
            raise UnauthorizedAccessException()

        logger.info(f"Successfully retrieved task ID: {task_id} for user ID: {user_id}")
        return task
    except ValueError:
        # Invalid UUID format
        logger.warning(f"Invalid UUID format for task ID: {task_id} or user ID: {user_id}")
        raise TaskNotFoundException(task_id)


def update_task(session: Session, task_id: str, task_update: TaskUpdate, user_id: str) -> Task:
    """
    Update a specific task for a user.

    Args:
        session: Database session
        task_id: ID of the task to update
        task_update: Task update data
        user_id: ID of the user who owns the task

    Returns:
        Task: The updated task

    Raises:
        TaskNotFoundException: If the task doesn't exist
        UnauthorizedAccessException: If the user doesn't own the task
    """
    import uuid

    logger.info(f"Updating task ID: {task_id} for user ID: {user_id}")

    try:
        # Convert the user_id string to UUID
        user_uuid = uuid.UUID(user_id) if not isinstance(user_id, uuid.UUID) else user_id

        # Convert the task_id string to UUID for comparison
        task_uuid = uuid.UUID(task_id) if not isinstance(task_id, uuid.UUID) else task_id

        statement = select(Task).where(Task.id == task_uuid)
        task = session.exec(statement).first()

        if not task:
            logger.warning(f"Attempt to update non-existent task ID: {task_id}")
            raise TaskNotFoundException(task_id)

        if task.user_id != user_uuid:
            logger.warning(f"User {user_id} attempted to update task {task_id} owned by user {task.user_id}")
            raise UnauthorizedAccessException()

        # Update the task with provided values
        update_data = task_update.dict(exclude_unset=True)

        # Only update fields that are explicitly provided
        for field, value in update_data.items():
            if hasattr(task, field):
                # Handle the status field specially if it's a string
                if field == "status" and isinstance(value, str):
                    # Convert string status to TaskStatus enum
                    try:
                        status_enum = TaskStatus(value.lower())
                        setattr(task, field, status_enum)
                    except ValueError:
                        logger.warning(f"Invalid status value: {value}")
                        raise ValueError(f"Invalid status: {value}. Must be 'pending' or 'completed'.")
                elif value is not None:
                    setattr(task, field, value)

        # Always update the timestamp
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"Successfully updated task ID: {task_id}")
        return task
    except ValueError:
        # Invalid UUID format
        logger.warning(f"Invalid UUID format for task ID: {task_id} or user ID: {user_id}")
        raise TaskNotFoundException(task_id)


def delete_task(session: Session, task_id: str, user_id: str) -> None:
    """
    Delete a specific task for a user.

    Args:
        session: Database session
        task_id: ID of the task to delete
        user_id: ID of the user who owns the task

    Raises:
        TaskNotFoundException: If the task doesn't exist
        UnauthorizedAccessException: If the user doesn't own the task
    """
    import uuid

    logger.info(f"Deleting task ID: {task_id} for user ID: {user_id}")

    try:
        # Convert the user_id string to UUID
        user_uuid = uuid.UUID(user_id) if not isinstance(user_id, uuid.UUID) else user_id

        # Convert the task_id string to UUID for comparison
        task_uuid = uuid.UUID(task_id) if not isinstance(task_id, uuid.UUID) else task_id

        statement = select(Task).where(Task.id == task_uuid)
        task = session.exec(statement).first()

        if not task:
            logger.warning(f"Attempt to delete non-existent task ID: {task_id}")
            raise TaskNotFoundException(task_id)

        if task.user_id != user_uuid:
            logger.warning(f"User {user_id} attempted to delete task {task_id} owned by user {task.user_id}")
            raise UnauthorizedAccessException()

        session.delete(task)
        session.commit()

        logger.info(f"Successfully deleted task ID: {task_id}")
    except ValueError:
        # Invalid UUID format
        logger.warning(f"Invalid UUID format for task ID: {task_id} or user ID: {user_id}")
        raise TaskNotFoundException(task_id)
    except Exception as e:
        logger.error(f"Error deleting task ID {task_id} for user {user_id}: {str(e)}")
        # Rollback the transaction in case of error
        session.rollback()
        raise


def toggle_task_completion(session: Session, task_id: str, completed: bool, user_id: str) -> Task:
    """
    Toggle the completion status of a task.

    Args:
        session: Database session
        task_id: ID of the task to update
        completed: Whether the task should be marked as completed
        user_id: ID of the user who owns the task

    Returns:
        Task: The updated task

    Raises:
        TaskNotFoundException: If the task doesn't exist
        UnauthorizedAccessException: If the user doesn't own the task
    """
    import uuid

    logger.info(f"Toggling completion status for task ID: {task_id} (completed: {completed}) for user ID: {user_id}")

    try:
        # Convert the user_id string to UUID
        user_uuid = uuid.UUID(user_id) if not isinstance(user_id, uuid.UUID) else user_id

        # Convert the task_id string to UUID for comparison
        task_uuid = uuid.UUID(task_id) if not isinstance(task_id, uuid.UUID) else task_id

        statement = select(Task).where(Task.id == task_uuid)
        task = session.exec(statement).first()

        if not task:
            logger.warning(f"Attempt to toggle completion for non-existent task ID: {task_id}")
            raise TaskNotFoundException(task_id)

        if task.user_id != user_uuid:
            logger.warning(f"User {user_id} attempted to toggle task {task_id} owned by user {task.user_id}")
            raise UnauthorizedAccessException()

        # Update the status
        task.status = TaskStatus.completed if completed else TaskStatus.pending
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"Successfully toggled completion status for task ID: {task_id}")
        return task
    except ValueError:
        # Invalid UUID format
        logger.warning(f"Invalid UUID format for task ID: {task_id} or user ID: {user_id}")
        raise TaskNotFoundException(task_id)
    except Exception as e:
        logger.error(f"Error toggling completion status for task ID {task_id} for user {user_id}: {str(e)}")
        # Rollback the transaction in case of error
        session.rollback()
        raise