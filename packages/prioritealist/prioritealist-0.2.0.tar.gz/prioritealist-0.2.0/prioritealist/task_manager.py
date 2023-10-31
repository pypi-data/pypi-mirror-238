"""
Main file for PrioriTealist
"""
import uuid
from typing import List
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)


class Task:
    """
    Class to define a task
    """

    def __init__(self, task_name: str, task_category: str, due_date: str) -> None:
        """
        Construct all the necessary attributes for the task object.

        :param task_name: The name of the task
        :type task_name: str
        :param task_category: The category of the task
        :type task_category: str
        :param due_date: The tasks due date
        :type due_date: str

        """
        self.task_name = task_name
        self.task_category = task_category
        self.due_date = due_date
        self.status = False
        logging.info("The task %s has been successfully created !", self.task_name)

    def __repr__(self):
        """
        Renders the class name
        """
        return (
            f"{self.__class__.__name__}(task_name= {self.task_name!r},"
            f"task_category={self.task_category!r}, due_date={self.due_date!r})"
        )


class PrioriTeaList:
    """
    Class to define the task list
    """

    def __init__(self) -> None:
        """
        Construct all the necessary attribute for the task list.
        The task_list dictionary links task names by their IDs.
        The task_mapper dictionary links the task IDs by their names.
        """
        self.task_list: dict = {}
        self.task_mapper: dict = {}
        logging.info("Task list initialization")

    def add_task(self, task: Task) -> None:
        """
        Add a new task to the list.

        :param task: The Task object to add
        :type task: Task
        """
        unique_id = str(uuid.uuid4())
        if task.task_name in self.task_mapper:
            logging.error("KeyError while adding task: %s", task.task_name)
            raise KeyError(f"Task with name '{task.task_name}' already exists.")
        self.task_list[unique_id] = {
            "task": task.task_name,
            "category": task.task_category,
            "due_date": task.due_date,
            "status": task.status,
        }
        self.task_mapper[task.task_name] = unique_id
        logging.info(
            "The task %s has been successfully added to the task list !",
            task.task_name,
        )

    def complete_task(self, task_name: str) -> None:
        """
        Changes a task's status to completed

        :param task_name: The name of the task to complete
        :type task_name: str
        """
        active_unique_id = self.task_mapper.get(task_name)
        if active_unique_id is None:
            error_message = (
                f"Task with name '{task_name}' not found in the list of tasks."
            )
            logging.error("KeyError while completing task: %s", error_message)
            raise KeyError(error_message)
        self.task_list[active_unique_id]["status"] = True
        logging.info("The task %s has been successfully completed !", task_name)

    def remove_task(self, task_name: str) -> None:
        """
        Remove a specific task from the task list

        :param task_name: The name of the task to remove
        :type task_name: str
        """
        active_unique_id = self.task_mapper.get(task_name)
        if active_unique_id is None:
            error_message = (
                f"Task with name '{task_name}' not found in the list of tasks."
            )
            logging.error("KeyError while removing task: %s", error_message)
            raise KeyError(error_message)
        del self.task_list[active_unique_id]
        del self.task_mapper[task_name]
        logging.info(
            "The task %s has been successfully removed from the task list !",
            task_name,
        )

    def show_tasks(self) -> List:
        """
        Show the entire tasks and their attributes. Return all the values of the list.

        :return: The list of tasks to show
        :rtype: List
        """
        return list(self.task_list.values())
