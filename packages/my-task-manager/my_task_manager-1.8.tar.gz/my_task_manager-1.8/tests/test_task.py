"""
Test Suite for Task Management Application

This test suite contains test cases for the Task Management Application, covering various aspects of the application.

Test Cases:
    - test_create_task_with_name_and_description(): Test creating a task with a name and description.
    - test_mark_task_as_completed(): Test marking a task as completed.
    - test_print_task_string_representation(): Test the string representation of a task.
    - test_unique_task_ids(): Test creating multiple tasks with unique IDs.
    - test_create_task_with_empty_name_or_description(): Test creating a task with an empty name or description.
    - test_mark_task_as completed_multiple_times(): Test marking a task as completed multiple times.

Each test case verifies specific functionality or behavior of the application.

Example:
    test_create_task_with_name_and_description()
    test_mark_task_as_completed()

    Output:
    - Verifies that the task is created with the correct name and description.
    - Verifies that the task is correctly marked as completed.

"""


from tasks.task import Task

import pytest


class TestCodeUnderTest:

    # create a task with a name and description
    def test_create_task_with_name_and_description(self):
        """
        Test creating a task with a name and a description.
        Verifies that the name and description are correctly set.
        """
        task = Task("Task 1", "Description 1")
        assert task.name == "Task 1"
        assert task.description == "Description 1"

    # mark a task as completed
    def test_mark_task_as_completed(self):
        """
        Test marking a task as completed.
        Verifies that the task is correctly marked as completed.
        """
        task = Task("Task 1", "Description 1")
        assert task.completed is False
        task.mark_completed()
        assert task.completed is True

    # print a task's string representation
    def test_print_task_string_representation(self):
        """
        Test the string representation of a task.
        Verifies that the generated string matches the expected format.
        """
        task = Task("Task 1", "Description 1")
        id = task.id
        expected_output = "ID : " + \
            str(id) + "\nTâche : Task 1\nDescription : Description 1\nStatut : Non terminée\nDate de création : " + \
            str(task.created_date) + "\n"
        assert str(task) == expected_output

    # create multiple tasks and check if their IDs are unique
    def test_unique_task_ids(self):
        """
        Test creating multiple tasks.
        Verifies that the IDs of the created tasks are unique.
        """
        task1 = Task("Task 1", "Description 1")
        task2 = Task("Task 2", "Description 2")
        task3 = Task("Task 3", "Description 3")
        assert task1.id != task2.id
        assert task1.id != task3.id
        assert task2.id != task3.id

    # create a task with an empty name or description
    def test_create_task_with_empty_name_or_description(self):
        """
        Tests the creation of a task with an empty name or description.
        Checks that an exception is thrown when the name or description is empty.
        """
        with pytest.raises(Exception):
            Task("", "Description 1")
        with pytest.raises(Exception):
            Task("Task 1", "")

    # mark a task as completed multiple times
    def test_mark_task_as_completed_multiple_times(self):
        """
        Test marking a task as completed multiple times.
        Verifies that the status of task remains marked as demanded.
        """
        task = Task("Task 1", "Description 1")
        assert task.completed is False
        task.mark_completed()
        assert task.completed is True
        task.mark_completed()
        assert task.completed is True
