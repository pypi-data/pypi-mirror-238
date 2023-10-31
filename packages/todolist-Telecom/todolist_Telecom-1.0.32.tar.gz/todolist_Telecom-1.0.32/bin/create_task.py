"""Add a new task to the todolist."""

import argparse
import logging
import re
from datetime import datetime
from models.task import Task


def create_task():
    """Create a new task instance."""
    logging.basicConfig(filename='logs/create_task.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s: %(message)s')

    parser = argparse.ArgumentParser(description='Create a new task')
    parser.add_argument('name', type=str, nargs='?',
                        help='the name of the new task')
    args = parser.parse_args()

    if args.name:
        task_name = args.name
    else:
        task_name = input("Enter the name of the new task: ")

    # ask for description and date
    description = input("Enter the description of the new task: ")
    start_date = input(
        "Enter the date when the task should start (YYYY-MM-DD): ")
    end_date = input("Enter the date when the task should end (YYYY-MM-DD): ")

    start_date = start_date.replace(" ", "")
    end_date = end_date.replace(" ", "")

    # check if date is in correct format
    date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')
    if not date_regex.match(start_date):
        logging.error(
            "Failed to create task: Invalid start date format '%s'",
            start_date)
        raise ValueError("Invalid date format. Please use YYYY-MM-DD format.")

    if not date_regex.match(end_date):
        logging.error(
            "Failed to create task: Invalid end date format '%s'", end_date)
        raise ValueError("Invalid date format. Please use YYYY-MM-DD format.")

    # create a new task instance
    try:
        new_task = Task(name=task_name, description=description,
                        start_at=datetime.strptime(start_date, "%Y-%m-%d"),
                        end_at=datetime.strptime(end_date, "%Y-%m-%d"))
        logging.info("Task '%s' created successfully", new_task.name)
        start_date = new_task.start_at.strftime("%Y-%m-%d")
        end_date = new_task.end_at.strftime("%Y-%m-%d")
        print(
            f"Task '{task_name}' created successfully")
    except (ValueError, TypeError) as e:
        logging.error("Failed to create task: %s", e)


if __name__ == '__main__':
    create_task()
