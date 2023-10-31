"""This script list all the of a user in the database."""

from models.task_list import TaskList
from models.db import execute_query


def list_tasks(user_id: int):
    """List all the of a user in the database."""
    task_list = TaskList()

    query = "SELECT * FROM tasks INNER JOIN assigned_to ON id = id_task where u.id = ?"
    values = (user_id,)

    results = execute_query(query, values)
    print(results)
    for result in results:
        task_list.add_task(result[1], result[2])
