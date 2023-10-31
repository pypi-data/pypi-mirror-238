"""Module for managing individual users in a todolist."""


class User:
    """Represent an individue in a todolist.

    Attributes:
        id: A unique identifier for the task.
        name: The name of the task.
        password: The users passeword.
    """

    def __init__(self, name: str, password: str = ""):
        """Initialize a new Task instance.

        Args:
            name (str): The name of the users.
            password (str): The password of the users.
            Defaults to an empty string.
        """
        self.id = id(self)  # Unique ID
        self.name = name
        self.password = password
