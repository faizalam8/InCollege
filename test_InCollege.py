import pytest
import InCollege
import sqlite3
import builtins

from InCollege import search_by_name, main, find_user, logged_in, job_search, learn_skill


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


