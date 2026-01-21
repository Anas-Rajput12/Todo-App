from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
import re
from datetime import datetime

from ..database import get_session
from ..models.task import Task, TaskCreate, TaskRead, TaskUpdate, TaskStatus
from ..models.user import UserRead
from ..services.task_service import (
    create_task, get_tasks, get_task, update_task, delete_task, toggle_task_completion
)
from ..middleware.auth import JWTBearer
from ..utils.exceptions import TaskNotFoundException, UnauthorizedAccessException
from ..utils.logging_config import setup_logging
from typing import Dict, Any

# Set up logging
logger = setup_logging()

router = APIRouter()


def sanitize_text(text: str, max_length: int = 200) -> str:
    """Sanitize text input by stripping whitespace and limiting length."""
    if not text:
        return text

    # Strip leading/trailing whitespace
    sanitized = text.strip()

    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    # Remove potentially dangerous characters (basic sanitization)
    # This is a simple approach - for production, consider using a library like bleach
    sanitized = re.sub(r'<[^>]*>', '', sanitized)  # Remove HTML tags
    sanitized = sanitized.replace('\0', '')  # Remove null bytes

    return sanitized


def validate_task_title(title: str) -> list:
    """Validate task title and return list of validation errors."""
    errors = []

    if not title or len(title.strip()) == 0:
        errors.append("Title is required")
    elif len(title.strip()) < 1:
        errors.append("Title must be at least 1 character long")
    elif len(title) > 200:
        errors.append("Title must be no more than 200 characters")

    # Check for potentially dangerous content
    if re.search(r'<script|javascript:|on\w+\s*=|<iframe', title, re.IGNORECASE):
        errors.append("Title contains invalid characters or code")

    return errors


def validate_task_description(description: str) -> list:
    """Validate task description and return list of validation errors."""
    errors = []

    if description and len(description) > 1000:
        errors.append("Description must be no more than 1000 characters")

    # Check for potentially dangerous content
    if description and re.search(r'<script|javascript:|on\w+\s*=|<iframe', description, re.IGNORECASE):
        errors.append("Description contains invalid characters or code")

    return errors


@router.get("/", response_model=Dict[str, List[TaskRead]])
def read_tasks(
    current_user: UserRead = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the current user.

    Args:
        current_user: The currently authenticated user
        session: Database session

    Returns:
        Dict: Dictionary containing a list of tasks
    """
    try:
        user_tasks = get_tasks(session, str(current_user.id))
        return {"tasks": user_tasks}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving tasks"
        )


@router.post("/", response_model=TaskRead)
def create_new_task(
    task: TaskCreate,
    current_user: UserRead = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the current user.

    Args:
        task: Task creation data
        current_user: The currently authenticated user
        session: Database session

    Returns:
        TaskRead: The created task
    """
    try:
        # Validate input data
        title_errors = validate_task_title(task.title)
        if title_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title validation failed: " + "; ".join(title_errors)
            )

        description_errors = validate_task_description(task.description)
        if description_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description validation failed: " + "; ".join(description_errors)
            )

        # Sanitize inputs
        task.title = sanitize_text(task.title, 200)
        if task.description:
            task.description = sanitize_text(task.description, 1000)

        logger.info(f"Creating new task for user ID: {current_user.id}")
        created_task = create_task(session, task, str(current_user.id))
        logger.info(f"Successfully created task ID: {created_task.id} for user ID: {current_user.id}")
        return created_task
    except HTTPException:
        logger.warning(f"HTTP exception while creating task for user ID: {current_user.id}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while creating task for user ID {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the task"
        )


@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: str,
    current_user: UserRead = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the current user.

    Args:
        task_id: The ID of the task to retrieve
        current_user: The currently authenticated user
        session: Database session

    Returns:
        TaskRead: The requested task
    """
    try:
        task = get_task(session, task_id, str(current_user.id))
        return task
    except TaskNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    except UnauthorizedAccessException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving the task"
        )


@router.put("/{task_id}", response_model=TaskRead)
def update_existing_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: UserRead = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID for the current user.

    Args:
        task_id: The ID of the task to update
        task_update: Task update data
        current_user: The currently authenticated user
        session: Database session

    Returns:
        TaskRead: The updated task
    """
    try:
        # Validate task_id format (basic validation)
        if not task_id or len(task_id) < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid task ID"
            )

        # Validate and sanitize inputs if they exist
        if task_update.title is not None:
            title_errors = validate_task_title(task_update.title)
            if title_errors:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Title validation failed: " + "; ".join(title_errors)
                )
            task_update.title = sanitize_text(task_update.title, 200)

        if task_update.description is not None:
            description_errors = validate_task_description(task_update.description)
            if description_errors:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Description validation failed: " + "; ".join(description_errors)
                )
            task_update.description = sanitize_text(task_update.description, 1000)

        # Validate status if provided
        if task_update.status is not None:
            if task_update.status not in ["pending", "completed"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Status must be either 'pending' or 'completed'"
                )

        logger.info(f"Updating task ID: {task_id} for user ID: {current_user.id}")
        updated_task = update_task(session, task_id, task_update, str(current_user.id))
        logger.info(f"Successfully updated task ID: {task_id} for user ID: {current_user.id}")
        return updated_task
    except TaskNotFoundException:
        logger.warning(f"Task with ID {task_id} not found for user ID: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    except UnauthorizedAccessException:
        logger.warning(f"Unauthorized update attempt to task {task_id} by user ID: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    except HTTPException:
        logger.warning(f"HTTP exception while updating task {task_id} for user ID: {current_user.id}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while updating task {task_id} for user ID {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating the task"
        )


@router.delete("/{task_id}")
def delete_existing_task(
    task_id: str,
    current_user: UserRead = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID for the current user.

    Args:
        task_id: The ID of the task to delete
        current_user: The currently authenticated user
        session: Database session

    Returns:
        None: Empty response with 204 status code
    """
    try:
        delete_task(session, task_id, str(current_user.id))
        return None  # 204 No Content is the default for delete with no return value
    except TaskNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    except UnauthorizedAccessException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the task"
        )


@router.patch("/{task_id}/complete", response_model=TaskRead)
async def toggle_task_completion_status(
    task_id: str,
    completed: Dict[str, bool],
    current_user: UserRead = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task.

    Args:
        task_id: The ID of the task to update
        completed: Dictionary with 'completed' boolean value
        current_user: The currently authenticated user
        session: Database session

    Returns:
        TaskRead: The updated task
    """
    try:
        # Validate task_id format (basic validation)
        if not task_id or len(task_id) < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid task ID"
            )

        # Validate the completed parameter
        if not isinstance(completed, dict) or "completed" not in completed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request body must contain 'completed' field with boolean value"
            )

        completed_status = completed["completed"]
        if not isinstance(completed_status, bool):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="'completed' field must be a boolean value"
            )

        logger.info(f"Setting completion status for task ID: {task_id} to: {completed_status} for user ID: {current_user.id}")
        updated_task = toggle_task_completion(session, task_id, completed_status, str(current_user.id))
        logger.info(f"Successfully updated completion status for task ID: {task_id} for user ID: {current_user.id}")
        return updated_task
    except TaskNotFoundException:
        logger.warning(f"Task with ID {task_id} not found for user ID: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    except UnauthorizedAccessException:
        logger.warning(f"Unauthorized update attempt to task {task_id} by user ID: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    except HTTPException:
        logger.warning(f"HTTP exception while updating task {task_id} status for user ID: {current_user.id}")
        raise
    except ValueError as ve:
        # Handle UUID conversion errors specifically
        logger.error(f"UUID conversion error while updating task {task_id} status for user ID {current_user.id}: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )
    except Exception as e:
        logger.error(f"Unexpected error while updating task {task_id} status for user ID {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating the task status"
        )