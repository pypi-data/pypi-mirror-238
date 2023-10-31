"""Database module for the application."""

import sqlite3


def connect():
    """Connect to the database and return a connection object."""
    conn = sqlite3.connect('To_do_list.db')
    return conn


def execute_query(query, params=None):
    """Execute a SQL query and return the results."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return results
