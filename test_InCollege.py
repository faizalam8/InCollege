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


# def test_job_search_go_back(capsys):
#     user_inputs = ["1", "3"]
#     user_inputs_iter = iter(user_inputs)

#     def simulate_user_input():
#         try:
#             return next(user_inputs_iter)
#         except StopIteration:
#             return ""
        
#     original_input = builtins.input
#     builtins.input = simulate_user_input  

#     job_search()  

#     captured = capsys.readouterr()

#     builtins.input = original_input

#     assert "3. Go Back" in captured.out
#     assert "==========" in captured.out


def mock_input(monkeypatch):
    user_inputs = []
    user_inputs_iter = iter(user_inputs)

    def mock_input_func(prompt):
        try:
            return next(user_inputs_iter)
        except StopIteration:
            raise AssertionError("No more user inputs provided")

    monkeypatch.setattr('builtins.input', mock_input_func)

# Test case 1: User selects "Job Search" and then goes back
def test_job_search_go_back(mock_input, capsys):
    # Simulate user input: 1 (Job Search), 4 (Go Back)
    user_inputs = ["1", "4"]
    user_inputs_iter = iter(user_inputs)

    # Run the main function
    main()

    # Capture printed output
    captured = capsys.readouterr()

    # Verify that the user can go back from Job Search
    assert "4. Go Back" in captured.out
    assert "===========" in captured.out  # Main menu header should be displayed again

# Test case 2: User selects "User Search" and then goes back
def test_user_search_go_back(mock_input, capsys):
    # Simulate user input: 2 (User Search), 4 (Go Back)
    user_inputs = ["2", "4"]
    user_inputs_iter = iter(user_inputs)

    # Run the main function
    main()

    # Capture printed output
    captured = capsys.readouterr()

    # Verify that the user can go back from User Search
    assert "4. Go Back" in captured.out
    assert "===========" in captured.out  # Main menu header should be displayed again

# Test case 3: User selects "Learn Skill" and then goes back
def test_learn_skill_go_back(mock_input, capsys):
    # Simulate user input: 3 (Learn Skill), 6 (Go Back)
    user_inputs = ["3", "6"]
    user_inputs_iter = iter(user_inputs)

    # Run the main function
    main()

    # Capture printed output
    captured = capsys.readouterr()

    # Verify that the user can go back from Learn Skill
    assert "6. Go Back" in captured.out
    assert "===========" in captured.out  # Main menu header should be displayed again