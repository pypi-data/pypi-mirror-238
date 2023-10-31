"""
Task List Management Module.

This module defines a `TaskList` class for managing a list of tasks.
The class maintains two lists: `tasks` for active tasks and `archived_tasks` for completed tasks.
It provides methods for adding, removing, and archiving tasks, as well as displaying the details of tasks.

Classes:
    TaskList: Manages a list of tasks and provides task-related operations.

Attributes:
    - tasks (list): A list of active Task objects.
    - archived_tasks (list): A list of completed Task objects.

Methods:
    - add_task(name, description): Add a new task to the list.
    - remove_task(task_name): Remove a task from the list.
    - mark_task_completed(task_name): Mark a task as completed and move it to archived tasks.
    - display_tasks(): Display details of active tasks.
    - display_archived_tasks(): Display details of completed tasks.

Example:
    task_list = TaskList()
    task_list.add_task("Task 1", "Description 1")
    task_list.display_tasks()

    Output:
    ID : 0
    Task : Task 1
    Description : Description 1
    Status : Not completed
    Created Date : <current date and time>
"""


from .task import Task
import logging
debug_logger = logging.getLogger("debug_logger")
error_logger = logging.getLogger("error_logger")


class TaskList:
    """
    A class for managing a list of tasks.

    Attributes:
        tasks (list): A list of Task objects representing the current tasks.
        archived_tasks (list): A list of Task objects representing the completed tasks.

    Methods:
        add_task(name, description): Adds a new task to the tasks list.
        remove_task(task_name): Removes a task from the tasks list.
        mark_task_completed(task_name): Marks a task as completed and moves it to the archived tasks list.
        display_tasks(): Displays the details of each task in the tasks list.
        display_archived_tasks(): Displays the details of each task in the archived tasks list.
    """

    def __init__(self):
        """
        Initialize a TaskList object.

        The `TaskList` class is used for managing a list of tasks, including active tasks
        and archived tasks. During initialization, it creates two empty lists, `tasks`
        for active tasks and `archived_tasks` for completed tasks.

        Example:
        task_list = TaskList()
        task_list.add_task("Task 1", "Description 1")
        task_list.display_tasks()

        Outputs:
        ID: 0
        Task: Task 1
        Description: Description 1
        Status: Not completed
        Created Date: <current date and time>
        """
        self.tasks = []
        self.archived_tasks = []
        debug_logger.debug("Nouvelle liste de tâches créée.")

    def add_task(self, name, description):
        """
        Add a new task to the tasks list.

        Args:
            name (str): The name of the task.
            description (str): The description of the task.

        Returns:
            None
        """
        task = Task(name, description)
        self.tasks.append(task)
        logging.info("Tâche '%s' ajoutée à la liste.", task.name)

    def remove_task(self, task_name):
        """
        Remove a task from the tasks list.

        Args:
            task_name (str): The name of the task to be removed.

        Returns:
            None
        """
        for task in self.tasks:
            if task.name == task_name:
                self.tasks.remove(task)
                logging.info("Tâche '%s' supprimé de la liste.", task_name)
                return
        print(f"Tâche '{task_name}' introuvable dans la liste.")
        error_logger.error(f"Tâche '{task_name}' introuvable dans la liste.")

    def mark_task_completed(self, task_name):
        """
        Mark a task as completed and moves it to the archived tasks list.

        Args:
            task_name (str): The name of the task to be marked as completed.

        Returns:
            None
        """
        for task in self.tasks:
            if task.name == task_name:
                task.mark_completed()
                self.archived_tasks.append(task)
                self.tasks.remove(task)
                info_message = f"Tâche '{task_name}' complétée."
                logging.info(info_message)
                debug_logger.debug(info_message)
                return
        print(f"Tâche '{task_name}' introuvable dans la liste.")
        error_message = f"Tâche '{task_name}' introuvable dans la liste."
        logging.error(error_message)
        error_logger.error(error_message)

    def display_tasks(self):
        """
        Display the details of each task in the tasks list.

        Returns:
            None
        """
        if not self.tasks:
            print("Aucune tâche dans la liste.")
        else:
            for task in self.tasks:
                print(task)

    def display_archived_tasks(self):
        """
        Display the details of each task in the archived tasks list.

        Returns:
            None
        """
        if not self.archived_tasks:
            print("Aucune tâche archivée.")
        else:
            for task in self.archived_tasks:
                print(task)
