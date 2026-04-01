"""
Task Manager for the Todo Management Console Application.
Task ID: T003, T005, T006, T007, T009
"""

from models import Task


class TaskValidationError(Exception):
    """
    Custom exception for task validation errors.
    Task ID: T009
    """
    pass


class TaskManager:
    """
    Manages list of tasks in memory and handles add, update, delete, list, and toggle operations.

    Task ID: T007
    """

    def __init__(self):
        """
        Initialize the TaskManager with an empty task list and starting ID counter.
        Task ID: T005, T006
        """
        self.tasks = []  # In-memory task storage using Python list
        self.next_id = 1  # Unique ID generation starting from 1

    def get_next_id(self):
        """
        Generate the next unique ID for a task.
        Task ID: T006

        Returns:
            int: The next unique ID to be assigned to a task
        """
        current_id = self.next_id
        self.next_id += 1
        return current_id

    def add_task(self, title, description=""):
        """
        Add a new task with title and optional description.
        Task ID: T012

        Args:
            title (str): Task title (required)
            description (str, optional): Task description. Defaults to "".

        Returns:
            Task: The newly created Task object

        Raises:
            TaskValidationError: If title is invalid
        """
        # Validation: Ensure title is not empty
        if not title or not title.strip():
            raise TaskValidationError("Task title cannot be empty")

        task_id = self.get_next_id()
        task = Task(task_id, title.strip(), description.strip())
        self.tasks.append(task)
        return task

    def list_tasks(self):
        """
        Retrieve all tasks in the system.
        Task ID: T017

        Returns:
            list: List of all Task objects
        """
        return self.tasks

    def get_task_by_id(self, task_id):
        """
        Find a task by its ID.
        Task ID: T023, T028, T033

        Args:
            task_id (int): The ID of the task to find

        Returns:
            Task or None: The task if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id, title=None, description=None):
        """
        Update title and/or description of an existing task.
        Task ID: T022

        Args:
            task_id (int): ID of the task to update
            title (str, optional): New task title. Defaults to None.
            description (str, optional): New task description. Defaults to None.

        Returns:
            bool: True if task was updated, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        if title is not None:
            task.title = title.strip() if title.strip() else task.title
        if description is not None:
            task.description = description.strip()

        return True

    def delete_task(self, task_id):
        """
        Remove a task by its ID.
        Task ID: T027

        Args:
            task_id (int): ID of the task to delete

        Returns:
            bool: True if task was deleted, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        self.tasks.remove(task)
        return True

    def toggle_task_status(self, task_id):
        """
        Change a task's completion status.
        Task ID: T032

        Args:
            task_id (int): ID of the task to update

        Returns:
            bool: True if task status was toggled, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        task.completed = not task.completed
        return True