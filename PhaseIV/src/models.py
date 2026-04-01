"""
Task model definition for the Todo Management Console Application.
Task ID: T003, T004
"""


class Task:
    """
    Represents a single todo item with unique integer ID, title (required),
    description (optional), and completion status (completed/pending).

    Task ID: T004
    """

    def __init__(self, task_id, title, description="", completed=False):
        """
        Initialize a new Task instance.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Task title (required)
            description (str, optional): Task description. Defaults to "".
            completed (bool, optional): Completion status. Defaults to False.
        """
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed

    def __str__(self):
        """
        String representation of the task for display purposes.

        Returns:
            str: Formatted string representation of the task
        """
        status = "Completed" if self.completed else "Pending"
        return f"ID: {self.id} | Title: {self.title} | Description: {self.description} | Status: {status}"

    def to_dict(self):
        """
        Convert the task to a dictionary representation.

        Returns:
            dict: Dictionary representation of the task
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }