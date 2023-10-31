"""Create a new user"""

import argparse
import getpass
import logging
import hashlib
from models.user import User
from models.db import execute_query


def create_user():
    """This function creates a new user."""

    logging.basicConfig(filename='logs/create_user.log',
                        level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

    parser = argparse.ArgumentParser(description='Create a new user')
    parser.add_argument('username', type=str, nargs='?',
                        help='the username for the new user')
    args = parser.parse_args()

    if args.username:
        username = args.username
    else:
        username = input("Enter the username for the new user: ")
    password = getpass.getpass(prompt='Enter password: ')
    confirm_password = getpass.getpass(prompt='Confirm password: ')
    while password != confirm_password:
        print('Passwords do not match. Please try again.')
        logging.warning('Passwords do not match for user %s', username)
        password = getpass.getpass(prompt='Enter password: ')
        confirm_password = getpass.getpass(prompt='Confirm password: ')

    # Hash the password using SHA-256
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    new_user = User(username, password_hash)

    # Insert the new user into the users table
    query = "INSERT INTO Personnes (username, password) VALUES (?, ?)"
    values = (new_user.name, new_user.password,)
    try:
        execute_query(query, values)
    except Exception as error:
        print(error)
        print(f'User {args.username} already exists')
        logging.warning('User %s already exists', new_user.name)
        return

    print(f'User {new_user.name} created successfully')
    logging.info('User %s created successfully', new_user.name)


if __name__ == '__main__':
    create_user()
