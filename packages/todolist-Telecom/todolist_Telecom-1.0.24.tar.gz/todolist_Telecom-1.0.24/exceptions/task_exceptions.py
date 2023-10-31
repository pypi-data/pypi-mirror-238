"""This module contains exceptions related to todolist tasks."""


class TaskError(Exception):
    """Basic exception for task-related errors."""

    pass


class TaskNotFoundError(TaskError):
    """Exception to indicate that a task has not been found."""

    pass
