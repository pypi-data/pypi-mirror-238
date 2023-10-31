"""Module for managing tasks in a task list."""

from typing import Optional
from typing import List
from datetime import datetime
from models.task import Task
from exceptions.task_exceptions import TaskNotFoundError


class TaskList:
    """A class to represent a list of tasks."""

    def __init__(self):
        """Initialize an empty list of tasks."""
        self.tasks: List[Task] = []

    def add_task(self, name: str, description: str,
                 start_at: Optional[datetime] = None, end_at: Optional[datetime] = None) -> None:
        """Add a new task to the list.

        Args:
            name (str): The name of the task.
            description (str): A description of the task.
        """
        if start_at and end_at:
            task = Task(name, description, start_at, end_at)
        else:
            task = Task(name, description)
        self.tasks.append(task)

    def to_do_task(self, task_name: str, start_at: datetime, end_at: datetime) -> None:
        """Mark a task as to do.

        Args:
            task_name (str): The name of the task to mark as to do.
            start_at (str): The start date of the task.
            end_at (str): The end date of the task.

        Raises:
            TaskNotFoundError: If the task with the given name is not found.
        """
        for task in self.tasks:
            if task.name == task_name:
                task.mark_as_to_do(start_at, end_at)
                return
        raise TaskNotFoundError("Task not found!")

    def doing_task(self, task_name: str) -> None:
        """Mark a task as doing.

        Args:
            task_name (str): The name of the task to mark as doing.

        Raises:
            TaskNotFoundError: If the task with the given name is not found.
        """
        for task in self.tasks:
            if task.name == task_name:
                task.mark_as_doing()
                return
        raise TaskNotFoundError("Task not found!")

    def succeeded_task(self, task_name: str) -> None:
        """Mark a task as complete.

        Args:
            task_name (str): The name of the task to mark as succeeded.

        Raises:
            TaskNotFoundError: If the task with the given name is not found.
        """
        for task in self.tasks:
            if task.name == task_name:
                task.mark_as_succeeded()
                return
        raise TaskNotFoundError("Task not found!")

    def failed_task(self, task_name: str) -> None:
        """Mark a task as failed.

        Args:
            task_name (str): The name of the task to mark as failed.

        Raises:
            TaskNotFoundError: If the task with the given name is not found.
        """
        for task in self.tasks:
            if task.name == task_name:
                task.mark_as_failed()
                return
        raise TaskNotFoundError("Task not found!")

    def remove_task(self, task_name: str) -> None:
        """Remove a task from the list.

        Args:
            task_name (str): The name of the task to remove.

        Raises:
            TaskNotFoundError: If the task with the given name is not found.
        """
        for task in self.tasks:
            if task.name == task_name:
                self.tasks.remove(task)
                return
        raise TaskNotFoundError("Task not found!")

    def display_to_do_tasks(self) -> List[str]:
        """Return a list of to do tasks.

        with their names and descriptions.

        Returns:
            List[str]: A list of to do tasks.
        """
        return [
            f"{task.name} - {task.description}"
            for task in self.tasks
            if task.status == "to do"
        ]

    def display_doing_tasks(self) -> List[str]:
        """Return a list of doing tasks.

        with their names and descriptions.

        Returns:
            List[str]: A list of doing tasks.
        """
        return [
            f"{task.name} - {task.description}"
            for task in self.tasks
            if task.status == "doing"
        ]

    def display_succeeded_tasks(self) -> List[str]:
        """Return a list of succeeded tasks.

        with their names and descriptions.

        Returns:
            List[str]: A list of succeeded tasks.
        """
        return [
            f"{task.name} - {task.description}"
            for task in self.tasks
            if task.status == "succeeded"
        ]

    def display_failed_tasks(self) -> List[str]:
        """Return a list of failed tasks.

        with their names and descriptions.

        Returns:
            List[str]: A list of failed tasks.
        """
        return [
            f"{task.name} - {task.description}"
            for task in self.tasks
            if task.status == "failed"
        ]

    def display_tasks(self) -> List[str]:
        """Return a list of uncompleted tasks.

        with their names and descriptions.

        Returns:
            List[str]: A list of uncompleted tasks.
        """
        return [
            f"{task.name} - {task.description}"
            for task in self.tasks
            if task.status in ["to do", "doing"]
        ]
