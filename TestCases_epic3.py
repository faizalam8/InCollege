#Includes Epic 3 and 4 tests

import InCollege
import pytest
import sqlite3
from unittest.mock import patch, Mock, MagicMock
from InCollege import register, login, username_exists, num_registered_users, find_user, add_connection



conn = sqlite3.connect('fake_db.db')
db = conn.cursor()
db.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    first_name TEXT,
    last_name TEXT,
    email BOOLEAN,
    sms BOOLEAN,
    advertising BOOLEAN,
    language TEXT,
    university TEXT,
    major TEXT)''')

db.execute('''CREATE TABLE IF NOT EXISTS connections (
    user TEXT,
    username TEXT,
    FOREIGN KEY (user) REFERENCES users (username),
    FOREIGN KEY (username) REFERENCES users (username)
    )''')

db.execute('''
    CREATE TABLE IF NOT EXISTS friend_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_user TEXT,
    to_user TEXT,
    status INTEGER DEFAULT 0,
    FOREIGN KEY (from_user) REFERENCES users(username),
    FOREIGN KEY (to_user) REFERENCES users(username)
    )''')
def delete_fake_db():
    db.execute("DELETE FROM users")

@pytest.fixture
def conn():
    mock_conn = MagicMock()
    return mock_conn

#Epic 3 Tests
def test_about_page():
    with patch('builtins.input', side_effect=['6', '2', '1']):
        with patch('builtins.print') as mock_print:
            try:
                InCollege.main()
            except Exception as e:
                pass

            lines = [
                "In College: Welcome to In College, the world's largest college student network with many users in"
                " many countries and territories worldwide. This is some information about the history and purpose"
                " of the company.",
                '1. Go back'
            ]

            for line in lines:
                mock_print.assert_any_call(line)


def test_help_center():
    with patch('builtins.input', side_effect=['5', '1', '2']):
        with patch('builtins.print') as mock_print:
            InCollege.main()

            lines = [
                "We're here to help."
            ]

            for line in lines:
                mock_print.assert_any_call(line)


def test_blog():
    with patch('builtins.input', side_effect=['5', '1', '5']):
        with patch('builtins.print') as mock_print:
            InCollege.main()

            lines = [
                "Under construction"
            ]

            for line in lines:
                mock_print.assert_any_call(line)


def test_career():
    with patch('builtins.input', side_effect=['5', '1', '6']):
        with patch('builtins.print') as mock_print:
            InCollege.main()

            lines = [
                "Under construction"
            ]

            for line in lines:
                mock_print.assert_any_call(line)


def test_business_solutions():
    with patch('builtins.input', side_effect=['5', '3']):
        with patch('builtins.print') as mock_print:
            InCollege.main()

            lines = [
                "Under construction"
            ]

            for line in lines:
                mock_print.assert_any_call(line)


def test_directories():
    with patch('builtins.input', side_effect=['5', '4']):
        with patch('builtins.print') as mock_print:
            InCollege.main()

            lines = [
                "Under construction"
            ]

            for line in lines:
                mock_print.assert_any_call(line)



#EPIC 4 Testcases

@pytest.fixture
def mock_num_ten_users():
    with patch('InCollege.num_registered_users', return_value = 10) as _mock:
        yield _mock

# Make sure there are no more than 10 user accounts
def test_register_eleventh_user(mock_num_ten_users):
    delete_fake_db()
    with patch('InCollege.input', side_effect=["user11", "Password11!"]):
        with patch('builtins.print') as mock_print:
            register(conn)
    mock_print.assert_called_with("All permitted accounts have been created, please come back later")

#Test to see if it is possible to search for users by last name, university or major
def test_prompt_for_lastName_uni_or_major():
    user_inputs = ['Johnny','Depp', 'uni', 'major', 'johndoe', 'Password123!']

    with patch('builtins.input', side_effect=user_inputs) as mock_input, \
         patch('InCollege.username_exists', return_value=False), \
         patch('InCollege.find_user', return_value=False), \
         patch('InCollege.num_registered_users', return_value=0):

        # Mocking database connection and cursor
        mock_conn = Mock()
        mock_cursor = mock_conn.cursor.return_value
        InCollege.register(mock_conn)

        # Check if the user was prompted for last name, university, and major
        assert mock_input.call_count == 6
        assert mock_input.call_args_list[1][0][0] == 'Last name: '
        assert mock_input.call_args_list[2][0][0] == 'University name: '
        assert mock_input.call_args_list[3][0][0] == 'Major: '

        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO users (username, password, first_name, last_name, university, major, email, sms, advertising, language)"
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('johndoe', 'Password123!', 'Johnny', 'Depp', 'uni', 'major', True, True, True, 'English'))

'''
# Test to check if a friend request displays
def test_connection(conn, capsys):
    # Setup the global logged-in user's name
    global LOGGED_IN_FIRST, LOGGED_IN_LAST
    LOGGED_IN_FIRST = "John"
    LOGGED_IN_LAST = "Doe"

    connection_inputs = ["Johnny", "Depp", "johndoe"]
    with patch('InCollege.input', side_effect=connection_inputs):
        # Mock database connection
        with patch('InCollege.sqlite3.connect', return_value=conn):
            if conn.cursor().fetchone.return_value is not None:
                # Mock the response that there are 0 requests already displayed
                conn.cursor().fetchone.return_value = [0]

        # Execute add connection function
        InCollege.add_connection(LOGGED_IN_FIRST, LOGGED_IN_LAST)

        # Check if the job was inserted with the right details
        out, err = capsys.readouterr()
        assert out == "Success! Your request to add a friend is displayed.\n"
'''
