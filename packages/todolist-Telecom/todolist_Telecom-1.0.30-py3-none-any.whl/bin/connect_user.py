"""Connect a new user."""

import argparse
import getpass
import logging
import hashlib
from models.db import execute_query


def connect_user():
    """Verifie if the user and the password is correct."""
    logging.basicConfig(filename='logs/connect_user.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s: %(message)s')

    parser = argparse.ArgumentParser(description='Connect a user')
    parser.add_argument('username', type=str, nargs='?',
                        help='the username of user')
    args = parser.parse_args()

    if args.username:
        username = args.username
    else:
        username = input("Enter your username: ")

    password = getpass.getpass(prompt='Enter password: ')

    # Retrieve the hashed password for the given username
    query = "SELECT ID, password FROM Personnes WHERE username = ?"
    values = (username,)
    result = execute_query(query, values)
    if result is None:
        print(f'User {username} does not exist')
        logging.warning('User %s does not exist', username)
        return (None, False)

    hashed_password = result[0][1]
    print(hashed_password)

    # Hash the password entered by the user
    hashed_input_password = hashlib.sha256(password.encode()).hexdigest()

    # Compare the two hashed passwords
    if hashed_password == hashed_input_password:
        print(f'User {username} connected successfully')
        logging.info('User %s connected successfully', username)
        return (id, True)
    else:
        print('Incorrect password')
        logging.warning('Incorrect password for user %s', username)
        return (id, False)


if __name__ == '__main__':
    connect_user()
