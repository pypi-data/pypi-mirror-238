"""
Task Class - task.py.

This module defines the `Task` class, representing a task in the to-do list application.

The `Task` class includes the following attributes and methods:
- Attributes:
  - id (int): A unique identifier for the task.
  - name (str): The name of the task.
  - description (str): A description of the task.
  - completed (bool): A flag indicating whether the task is completed.
  - created_date (datetime): The date and time when the task was created.

- Methods:
  - __init__(self, name, description): Initializes a Task object with the provided name and description.
  The task is created with a unique ID, and completion status is set to False.
  - mark_completed(self): Marks the task as completed by setting the completion status to True.
  - __str__(self) -> str: Returns a formatted string representation of the task, including its ID,
  name, description, completion status, and creation date.

Exceptions:
- ValueError: If the name or description is not provided during task initialization.

This class is used to represent individual tasks within the to-do list application, allowing users to create,
manage, and mark tasks as completed. Each task has a unique identifier (ID) and associated information such as name,
description, completion status, and creation date.
"""


from datetime import datetime
import logging

debug_logger = logging.getLogger("debug_logger")
error_logger = logging.getLogger("error_logger")


class Task:
    """
    Task Class - task.py.

    This module defines the `Task` class, representing a task in the to-do list application.

    The `Task` class includes the following attributes and methods:
    - Attributes:
      - id (int): A unique identifier for the task.
      - name (str): The name of the task.
      - description (str): A description of the task.
      - completed (bool): A flag indicating whether the task is completed.
      - created_date (datetime): The date and time when the task was created.

    - Methods:
      - __init__(self, name, description): Initializes a Task object with the provided name and description.
      The task is created with a unique ID, and completion status is set to False.
      - mark_completed(self): Marks the task as completed by setting the completion status to True.
      - __str__(self) -> str: Returns a formatted string representation of the task, including its ID,
      name, description, completion status, and creation date.

    Exceptions:
    - ValueError: If the name or description is not provided during task initialization.

    This class is used to represent individual tasks within the to-do list application,
    allowing users to create, manage, and mark tasks as completed. Each task has a unique identifier (ID)
    and associated information such as name, description, completion status, and creation date.
    """

    _id_counter = 0

    def __init__(self, name, description):
        """
        Initialize a Task object.

        With a unique ID, name, description, completion status (False), and creation date (current datetime).

        Args:
            name (str): The name of the task.
            description (str): The description of the task.

        Raises:
            ValueError: If the name or description is not provided.
        """
        if not name:
            logging.error("Le nom doit être fourni pour une tâche.")
            raise ValueError("Le nom doit être fourni pour une tâche.")
        if not description:
            logging.error("La description doit être fournie pour une tâche.")
            raise ValueError(
                "La description doit être fournie pour une tâche.")

        self.id = Task._id_counter
        Task._id_counter += 1
        self.name = name
        self.description = description
        self.completed = False
        self.created_date = datetime.now()
        debug_logger.debug(f"Création d'une nouvelle tâche : {name}")

    def mark_completed(self):
        """Mark the task as completed by setting the completion status to True."""
        self.completed = True
        debug_logger.debug(
            f"La tâche '{self.name}' a été marquée comme terminée.")

    def __str__(self) -> str:
        """
        Return a string representation of the task, including its ID, name, description, completion status, and creation date.

        Returns:
            str: A formatted string representation of the task.
        """
        status = "Terminée" if self.completed else "Non terminée"
        return f"ID : {self.id}\nTâche : {self.name}\nDescription : {self.description}\nStatut : {status}\n" \
            f"Date de création : {self.created_date}\n"
