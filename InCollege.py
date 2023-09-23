import sqlite3

# Global vars to keep track of logged-in user
LOGGED_IN_FIRST = ""
LOGGED_IN_LAST = ""


def main():
    # Initialize database connection
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()
    # Create database if it doesn't already exist
    db.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT,
    first_name TEXT, last_name TEXT)''')
    # Close connection
    conn.close()
    print('=========================================================================')
    print('Welcome to InCollege! Would you like to log in or register a new account?')
    print('=========================================================================')

    print("SUCCESS STORY: I've been using InCollege for only three months and have managed to land "
          "two Software Engineering roles! This site has helped me obtain the necessary skills to "
          "apply, interview, and succeed in the industry.")
    print('1. Login')
    print('2. Register new account')
    print('3. Play video')
    print('4. Search by name')

    decision = input("")
    while decision != '1' and decision != '2' and decision != '3' and decision != '4':
        print('Please enter 1, 2, 3, or 4')
        decision = input("")

    if decision == '1':
        login()
    elif decision == '2':
        conn = sqlite3.connect('user_database.db')
        register(conn)
    elif decision == '3':
        print('Video is now playing')
        print('1. Go Back')
        decision = input("")
        while decision != '1':
            decision = input("")
        main()
    else:
        f_name = input("First: ")
        l_name = input("Last: ")
        search_by_name(f_name, l_name)


def search_by_name(f_name, l_name):
    # Query for user by name
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()
    db.execute("SELECT * FROM users WHERE first_name=? AND last_name=?", (f_name, l_name))
    user = db.fetchone()
    conn.close()

    if not user:
        print('They are not yet a part of the InCollege system yet')
        print('1. Go Back')
        decision = input("")
        while decision != '1':
            decision = input('')
        main()
    else:
        print('They are a part of the InCollege system')
        print('1. Go Back')
        decision = input("")
        while decision != '1':
            decision = input('')
        main()


def login():
    # Display login page
    print('===========')
    print('Login Page')
    print('===========')

    # Retrieve login information
    username = input('Enter username: ')
    password = input('Enter password: ')

    # Check if user exists and password is correct
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()
    db.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    output = db.fetchone()
    conn.close()

    if output is not None:
        global LOGGED_IN_FIRST, LOGGED_IN_LAST
        LOGGED_IN_FIRST = output[2]
        LOGGED_IN_LAST = output[3]
        print('You have successfully logged in')
        logged_in()
    else:
        print('Incorrect username / password, please try again')
        login()


def logged_in():
    # Display page once logged in
    print('==========')
    print('Home Page')
    print('==========')
    print('1. Job Search')
    print('2. User Search')
    print('3. Learn Skill')
    print('4. Logout')

    # Get user input
    decision = input("")
    while decision != '1' and decision != '2' and decision != '3' and decision != '4':
        print('Please enter 1, 2, 3, or 4')
        decision = input("")

    # Route input to proper function
    if decision == '1':
        job_search()
    elif decision == '2':
        find_user()
    elif decision == '3':
        learn_skill()
    else:
        # Empty global vars upon logout
        global LOGGED_IN_FIRST, LOGGED_IN_LAST
        LOGGED_IN_FIRST, LOGGED_IN_LAST = "", ""
        main()


def job_search():
    print('=====')
    print('Jobs')
    print('=====')

    # Create jobs database
    conn = sqlite3.connect("jobs.db")
    db = conn.cursor()
    db.execute('''CREATE TABLE IF NOT EXISTS jobs (title TEXT PRIMARY KEY,description TEXT,employer TEXT,
    location TEXT,salary TEXT, firstName TEXT, lastName TEXT)''')
    conn.commit()
    conn.close()

    # Create new job or search for a job
    print('1. Search for a job')
    print('2. Post a job')
    print('3. Go back')
    decision = input("")
    while decision != '1' and decision != '2' and decision != '3':
        print('Please enter 1, 2, or 3')
        decision = input("")

    if decision == '2':
        post_job()
    elif decision == '3':
        logged_in()
    else:
        # JOB SEARCH IMPLEMENTATION [NOT COMPLETE]
        print('Under construction')
        print('1. Go back')
        decision = input("")
        while decision != "1":
            decision = input("")
        job_search()


def post_job():
    if num_jobs() >= 5:
        print('5 jobs have already been posted')
        print('1. Go back')
        decision = input("")
        while decision != "1":
            decision = input("")
        job_search()

    title = input("Job title: ")
    description = input("Description: ")
    employer = input("Employer: ")
    location = input("Location: ")
    salary = input("Salary: ")

    conn = sqlite3.connect("jobs.db")
    db = conn.cursor()
    db.execute('''INSERT INTO jobs (title, description, employer, location, salary, firstName, lastName)
     VALUES (?, ?, ?, ?, ?, ?, ?)''', (title, description, employer, location, salary, LOGGED_IN_FIRST, LOGGED_IN_LAST))
    conn.commit()
    conn.close()
    print("Success! Your job has been posted")


def find_user():
    # Search for user by username
    username_input = input("Username: ")
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()
    db.execute("SELECT 1 FROM users WHERE username=?", (username_input,))
    output = db.fetchone()
    conn.close()

    if output:
        print('User found!')
    else:
        print('User not found')

    print('1. Go back')
    decision = input("")
    while decision != "1":
        decision = input("")
    logged_in()


def learn_skill():
    print('======')
    print('Skills')
    print('======')
    print('1. Elevator Pitch')
    print('2. Behavioral Prep')
    print('3. Technical Prep')
    print('4. Public Speaking')
    print('5. Problem Solving')
    print('6. Go Back')

    decision = input("")
    while decision != '1' and decision != '2' and decision != '3' and decision != '4' and decision != '5'\
            and decision != '6':
        print("Enter 1 - 6 to make a selection")
        decision = input("")

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
        logged_in()

    print('1. Go back')
    decision = input("")
    while decision != "1":
        decision = input("")
    learn_skill()


def register(conn):
    # Ensure there are less than 5 registered users
    num_users = num_registered_users()
    if num_users >= 5:
        print("All permitted accounts have been created, please come back later")
        return
    print('==================')
    print('Registration Page')
    print('==================')

    # Retrieve names
    f_name = input('First name: ')
    l_name = input('Last name: ')
    username = input('Enter username: ')

    # Check if username exists
    while username_exists(username):
        print('This username is already taken. Please select another')
        username = input('Enter username: ')

    # Get password input
    password = input('Enter password: ')
    while (not any(char.isupper() for char in password) or
            not any(char.isdigit() for char in password) or
            not any(char in '!@#$%^&*()_+' for char in password) or
            len(password) < 8 or len(password) > 12):
        print('Password must contain a capital letter, a digit, a special character, '
              'and be between 8-12 characters in length')
        password = input('Enter password: ')

    # Insert account into database
    db = conn.cursor()
    db.execute("INSERT INTO users (username, password, first_name, last_name) VALUES (?, ?, ?, ?)",
               (username, password, f_name, l_name))

    conn.commit()
    conn.close()


def username_exists(username):
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()

    # Check if user exists in database
    db.execute("SELECT 1 FROM users WHERE username=?", (username,))
    output = db.fetchone()
    conn.close()
    return output is not None


def num_registered_users():
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()

    # Retrieve and return user count
    db.execute("SELECT COUNT(*) FROM users")
    result = db.fetchone()
    conn.close()
    return result[0]


def num_jobs():
    # Return total job count
    conn = sqlite3.connect("jobs.db")
    db = conn.cursor()
    db.execute("SELECT COUNT(*) FROM jobs")
    result = db.fetchone()
    conn.close()
    return result[0]


if __name__ == "__main__":
    main()
