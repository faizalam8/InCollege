# Epic 2 and 3 Tests
import pytest
import InCollege
import sqlite3
import builtins

from InCollege import search_by_name, main, find_user, logged_in, job_search, learn_skill
from unittest.mock import patch, Mock, MagicMock


@pytest.fixture
def setup_database():
    conn = sqlite3.connect(":memory:")
    db = conn.cursor()
    db.execute('''CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT, f_name TEXT, l_name TEXT)''')
    test_users = [
        ("john_doe", "Password1!", "John", "Doe"),
        ("alice_smith", "Password2!", "Alice", "Smith"),
    ]

    for user in test_users:
        db.execute("INSERT INTO users (username, password, f_name, l_name) VALUES (?, ?, ?, ?)", user)
    
    conn.commit()
    yield conn
    conn.close()


def test_search_by_name_user_found(setup_database):
    conn = setup_database
    db = conn.cursor()

    f_name = "John"
    l_name = "Doe"

    # check if user exists
    db.execute("SELECT * FROM users WHERE f_name=? AND l_name=?", (f_name, l_name))

    output = db.fetchone()
    if output is not None:
        print("They are a part of the InCollege system")
        pass
    else:
        print("They are not yet a part of the InCollege system yet")
        pytest.fail("Wrong")

def test_search_by_name_user_not_found(setup_database):
    conn = setup_database
    db = conn.cursor()

    f_name = "Jane"
    l_name = "Doe"

    # check if user exists
    db.execute("SELECT * FROM users WHERE f_name=? AND l_name=?", (f_name, l_name))
    output = db.fetchone()
    if output is not None:
        print("They are a part of the InCollege system")
        pytest.fail("Wrong")
    else:
        print("They are not yet a part of the InCollege system yet")
        pass

def test_find_user_found(setup_database):
    conn = setup_database
    db = conn.cursor()

    username = "john_doe"

    # check if username exists
    db.execute("SELECT * FROM users WHERE username=?", (username,))
    output = db.fetchone()
    if output is not None:
        print("User found!")
        pass
    else:
        print("User not found")
        pytest.fail("Wrong")

def test_find_user_not_found(setup_database):
    conn = setup_database
    db = conn.cursor()

    username = "jane_doe"

    # check if username exists
    db.execute("SELECT * FROM users WHERE username=?", (username,))
    output = db.fetchone()
    if output is not None:
        print("User found!")
        pytest.fail("Wrong")
    else:
        print("User not found")
        pass



def conn():
    mock_conn = MagicMock()
    return mock_conn

def test_policies():
    with patch('builtins.input', side_effect=['6', '9']):
        with patch('builtins.print') as mock_print:
            try:
                InCollege.main()
            except Exception as e:
                pass

            lines = [
                "Welcome to the policies section!",
                "1. A Copyright Notice\n"
                "2. About\n"
                "3. Accessibility\n"
                "4. User Agreement\n"
                "5. Privacy Policy\n"
                "6. Cookie Policy\n"
                "7. Copyright policy\n"
                "8. Brand policy\n"
                "9. Go back"
            ]

            for line in lines:
                mock_print.assert_any_call(line)

def test_useful_links():
    with patch('builtins.input', side_effect=['5', '5']):
        with patch('builtins.print') as mock_print:
            try:
                InCollege.main()
            except Exception as e:
                pass

            lines = [
                "Useful Links:",
                "1. General",
                "2. Browse InCollege",
                "3. Business Solutions",
                "4. Directories",
                "5. Go back"
            ]

            for line in lines:
                mock_print.assert_any_call(line)

def test_copyright_notice():
    with patch('builtins.input', side_effect=['6', '1', '1']):
        with patch('builtins.print') as mock_print:
            try:
                InCollege.main()
            except Exception as e:
                pass

            lines = [
                "Copyright Notice",
                "The software for this tool is open-source."
                " This means that anyone can view the code and submit their changes to it.",
                "1. Go back"
            ]

            for line in lines:
                mock_print.assert_any_call(line)

def test_accessibility():
    with patch('builtins.input', side_effect=['6', '3', '1']):
        with patch('builtins.print') as mock_print:
            try:
                InCollege.main()
            except Exception as e:
                pass

            lines = [
                "Accessibility",
                "We ensure to make our tool accessible to everyone. Please reach out to us if there is any issue",
                "1. Go back"
            ]

            for line in lines:
                mock_print.assert_any_call(line)

def test_user_agreement():
    with patch('builtins.input', side_effect=['6', '4', '1']):
        with patch('builtins.print') as mock_print:
            try:
                InCollege.main()
            except Exception as e:
                pass

            lines = [
                "User Agreement",
                "This is a legal agreement between you(the licensee) and the licensor. There will be no fee assessed by"
                " the licensor for the product. This policy will be updated regularly.",
                "1. Go back"
            ]

            for line in lines:
                mock_print.assert_any_call(line)

def test_privacy_policy():
    with patch('builtins.input', side_effect=['6', '5', '2']):
        with patch('builtins.print') as mock_print:
            try:
                InCollege.main()
            except Exception as e:
                pass

            lines = [
                "Privacy Policy",
                "We strive to make sure your data is handled correctly and in a confidential manner."
                " Please reach out to us if there has been any issues with it.",
                "1. Guest Controls",
                "2. Go back"
            ]

            for line in lines:
                mock_print.assert_any_call(line)

def test_guest_controls():
    with patch('builtins.input', side_effect=['6', '5', '1', '1']):
        with patch('builtins.print') as mock_print:
            try:
                InCollege.main()
            except Exception as e:
                pass

            lines = [
                "You must login to access this page",
                "1. Go back"
            ]

            for line in lines:
                mock_print.assert_any_call(line)

def test_cookie_policy():
    with patch('builtins.input', side_effect=['6', '6', '1']):
        with patch('builtins.print') as mock_print:
            try:
                InCollege.main()
            except Exception as e:
                pass

            lines = [
                "Cookie Policy",
                "We only store essential cookies to make sure the user is authentic."
                " This is also done to prevent any security vulnerabilites.",
                "1. Go back"
            ]

            for line in lines:
                mock_print.assert_any_call(line)

def test_copyright_policy():
    with patch('builtins.input', side_effect=['6', '7', '1']):
        with patch('builtins.print') as mock_print:
            try:
                InCollege.main()
            except Exception as e:
                pass

            lines = [
                "Copyright Policy",
                "We have a copyright policy to make sure our product is not used in the wrong manner.",
                "1. Go back"
            ]

            for line in lines:
                mock_print.assert_any_call(line)
def test_brand_policy():
    with patch('builtins.input', side_effect=['6', '8', '1']):
        with patch('builtins.print') as mock_print:
            try:
                InCollege.main()
            except Exception as e:
                pass

            lines = [
                "Brand Policy",
                "We aim to make sure that each and every process in our software is consistent."
                " This policy is subject to further change",
                "1. Go back"
            ]

            for line in lines:
                mock_print.assert_any_call(line)


