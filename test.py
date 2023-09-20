import sqlite3
import pytest
from InCollege import job_search
from InCollege import find_user
from InCollege import learn_skill

@pytest.fixture
def test_database():
    conn = sqlite3.connect(':memory:')
    db = conn.cursor()
    db.execute('''CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT)''')
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("testuser", "password123"))
    conn.commit()
    yield conn
    conn.close()

def test_passed_login(test_database):
    #Used to interact with the database
    conn = test_database
    db = conn.cursor()

    # Display login page
    print('===========')
    print('Login Page')
    print('===========')

    #Login information
    username = 'testuser'
    password = 'password123'

    #Checks if the user exists and password is correct
    db.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    output = db.fetchone()

    if output is not None:
        print('You have successfully logged in')
        pass
    else:
        print('Incorrect username / password, please try again')
        pytest.fail("Wrong")

def test_failed_login(test_database):
    # The test_database fixture is automatically provided as an argument
    # Use it to interact with the database
    conn = test_database
    db = conn.cursor()

    # Display login page
    print('===========')
    print('Login Page')
    print('===========')

    # Retrieve login information
    username = 'username'
    password = 'password'

    # Check if user exists and password is correct
    db.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    output = db.fetchone()

    if output is not None:
        print('You have successfully logged in')
        pytest.fail("Wrong")
    else:
        print('Incorrect username / password, please try again')
        pass

def test_login_attempts(test_database):
    # The test_database fixture is automatically provided as an argument
    # Use it to interact with the database
    conn = test_database
    db = conn.cursor()

    # Counter to keep track of login attempts
    login_attempts = 0

    while login_attempts < 50:
        # Display login page
        print('===========')
        print('Login Page')
        print('===========')

        # Retrieve login information
        username = 'username'
        password = 'password'

        # Check if user exists and password is correct
        db.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        output = db.fetchone()

        if output is not None:
            print('You have successfully logged in')
            pytest.fail("Wrong")
        else:
            print('Incorrect username / password, please try again')
        
        login_attempts += 1

def test_job_search():
    print('Under construction')

def test_find_user():
    print('Under construction')

def test_learn_skill1():
    print('======')
    print('Skills')
    print('======')
    print('1. Elevator Pitch')
    print('2. Behavioral Prep')
    print('3. Technical Prep')
    print('4. Public Speaking')
    print('5. Problem Solving')
    print('6. Go Back')

    decision = 1
    '''while decision != '1' and decision != '2' and decision != '3' and decision != '4' and decision != '5'\
            and decision != '6':'''
    print("Enter 1 - 6 to make a selection")
    decision = 1

    if decision == '1':
        print("Under construction")
    elif decision == '2':
        print("Under construction")
    elif decision == '3':
        print("Under construction")
    elif decision == '4':
        print("Under construction")
    elif decision == '5':
        print("Under construction")
    else:
        print('logged_in()')

def test_learn_skill2():
    print('======')
    print('Skills')
    print('======')
    print('1. Elevator Pitch')
    print('2. Behavioral Prep')
    print('3. Technical Prep')
    print('4. Public Speaking')
    print('5. Problem Solving')
    print('6. Go Back')

    decision = 2
    '''while decision != '1' and decision != '2' and decision != '3' and decision != '4' and decision != '5'\
            and decision != '6':'''
    print("Enter 1 - 6 to make a selection")
    decision = 2

    if decision == '1':
        print("Under construction")
    elif decision == '2':
        print("Under construction")
    elif decision == '3':
        print("Under construction")
    elif decision == '4':
        print("Under construction")
    elif decision == '5':
        print("Under construction")
    else:
        print('logged_in()')
    
def test_learn_skill3():
    print('======')
    print('Skills')
    print('======')
    print('1. Elevator Pitch')
    print('2. Behavioral Prep')
    print('3. Technical Prep')
    print('4. Public Speaking')
    print('5. Problem Solving')
    print('6. Go Back')

    decision = 3
    '''while decision != '1' and decision != '2' and decision != '3' and decision != '4' and decision != '5'\
            and decision != '6':'''
    print("Enter 1 - 6 to make a selection")
    decision = 3

    if decision == '1':
        print("Under construction")
    elif decision == '2':
        print("Under construction")
    elif decision == '3':
        print("Under construction")
    elif decision == '4':
        print("Under construction")
    elif decision == '5':
        print("Under construction")
    else:
        print('logged_in()')

def test_learn_skill4():
    print('======')
    print('Skills')
    print('======')
    print('1. Elevator Pitch')
    print('2. Behavioral Prep')
    print('3. Technical Prep')
    print('4. Public Speaking')
    print('5. Problem Solving')
    print('6. Go Back')

    decision = 4
    '''while decision != '1' and decision != '2' and decision != '3' and decision != '4' and decision != '5'\
            and decision != '6':'''
    print("Enter 1 - 6 to make a selection")
    decision = 4

    if decision == '1':
        print("Under construction")
    elif decision == '2':
        print("Under construction")
    elif decision == '3':
        print("Under construction")
    elif decision == '4':
        print("Under construction")
    elif decision == '5':
        print("Under construction")
    else:
        print('logged_in()')

def test_learn_skill5():
    print('======')
    print('Skills')
    print('======')
    print('1. Elevator Pitch')
    print('2. Behavioral Prep')
    print('3. Technical Prep')
    print('4. Public Speaking')
    print('5. Problem Solving')
    print('6. Go Back')

    decision = 5
    '''while decision != '1' and decision != '2' and decision != '3' and decision != '4' and decision != '5'\
            and decision != '6':'''
    print("Enter 1 - 6 to make a selection")
    decision = 5

    if decision == '1':
        print("Under construction")
    elif decision == '2':
        print("Under construction")
    elif decision == '3':
        print("Under construction")
    elif decision == '4':
        print("Under construction")
    elif decision == '5':
        print("Under construction")
    else:
        print('logged_in()')
