"""Module for managing individual tasks in a todolist."""

from datetime import datetime
from typing import Optional


class Task:
    """Represent an individual task in a todolist.

    Attributes:
        id: A unique identifier for the task.
        name: The name of the task.
        description: A brief description of the task.
        created_at: The datetime when the task was created.
        start_at: The datetime when the task was started.
        end_at: The datetime when the task was ended.
        duration: The duration of the task.
        status: The status of the task (to_do, doing, succeeded, failed).
    """

    def __init__(self, name: str, description: Optional[str] = "",
                 start_at: Optional[datetime] = None, end_at: Optional[datetime] = None):
        """Initialize a new Task instance.

        Args:
            name (str): The name of the task.
            description (Optional[str], optional): A description for the task.
            Defaults to an empty string.
        """
        self.id = id(self)  # Unique ID
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.start_at = start_at
        self.end_at = end_at
        self.status = "to do"

    def mark_as_to_do(self, start_at: Optional[datetime] = None,
                      end_at: Optional[datetime] = None) -> None:
        """Mark a task as to do."""
        self.status = "to do"
        self.start_at = start_at
        self.end_at = end_at

    def mark_as_doing(self) -> None:
        """Mark a task as doing."""
        self.status = "doing"
        self.start_at = datetime.now()

    def mark_as_failed(self) -> None:
        """Mark a task as failed."""
        self.status = "failed"
        self.end_at = datetime.now()

    def mark_as_succeeded(self) -> None:
        """Mark a task as succeeded."""
        self.status = "succeeded"
        self.end_at = datetime.now()
