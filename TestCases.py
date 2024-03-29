# Epic 1 Test Cases
import InCollege
import pytest
import sqlite3
from unittest.mock import patch, Mock, MagicMock, call
from InCollege import register, login, username_exists

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
    major TEXT           
    )''')

def delete_fake_db():
    db.execute("DELETE FROM users")

@pytest.fixture 
def mock_num_registered_five_users():
    with patch('InCollege.num_registered_users', return_value = 10) as _mock:
        yield _mock
# Make sure there are no more than 5 user accounts
def test_register_sixth_user(mock_num_registered_five_users):
    delete_fake_db()
    with patch('InCollege.input', side_effect=["user6", "Password6!"]):
        with patch('builtins.print') as mock_print:
            register(conn)
    mock_print.assert_called_with("All permitted accounts have been created, please come back later")

# This is the test case for more than 5 users *** Tests Requirement No. 3 ***
# FIxure is used to mock the number of registered users
@pytest.fixture 
def mock_num_registered():
    with patch('InCollege.num_registered_users', return_value = 10) as _mock:
        yield _mock

# Check for max number of users 
def test_max_num_of_users(mock_num_registered):
    delete_fake_db()
    with patch('InCollege.input', side_effect =["testUser0", "testUser1!"] ):
        with patch('builtins.print') as mock_print:
            register(conn)
    mock_print.assert_called_with("All permitted accounts have been created, please come back later")

@pytest.fixture 
def mock_num_registered0():
    with patch('InCollege.num_registered_users', return_value = 0) as _mock:
        yield _mock
    
# Check that the password meets the set criteria for passwords 
def test_insecure_password(mock_num_registered0):
    delete_fake_db()
    with patch('InCollege.input', side_effect=["fname","lname", "uni", "major" "user34", "weakpass", "weakpass", "Secure@123"]): # Username and then a weak password
        with patch('builtins.print') as mock_print:
            register(conn)
    assert mock_print.mock_calls == [
        call('=================='),
        call('Registration Page'),
        call('=================='),
        call('Password must contain a capital letter, a digit, a special character, and be between 8-12 characters in length'),
    ]
    
# Test that the initial screen pops up
def test_initial_page_print():
    # Mock input to immediately return '1' for Login (to prevent further execution of main)
    with patch('InCollege.input', return_value='7'):
        # Mock database connection so real database isn't affected
        with patch('InCollege.sqlite3.connect', return_value=MagicMock()):
            # Capture printed output using the 'builtins.print' mock
            with patch('builtins.print') as mock_print:
                InCollege.main()
                
                # check the lines we expect to be printed
                lines = [
                        '=========================================================================',
                        'Welcome to InCollege! Would you like to log in or register a new account?',
                        '=========================================================================',

                        "SUCCESS STORY: I've been using InCollege for only three months and have managed to land "
                        "two Software Engineering roles! This site has helped me obtain the necessary skills to "
                        "apply, interview, and succeed in the industry.",
                    '1. Login',
                    '2. Register new account',
                    '3. Play video',
                    '4. Search by name',
                    '5. Useful Links',
                    '6. InCollege Important Links',
                    '7. Exit'
                ]
                
                for line in lines:
                    mock_print.assert_any_call(line)
        