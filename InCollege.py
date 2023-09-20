import sqlite3


def main():
    # Initialize database connection
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()
    # Create database if it doesn't already exist
    db.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    # Close connection
    conn.close()
    print('=========================================================================')
    print('Welcome to InCollege! Would you like to log in or register a new account?')
    print('=========================================================================')

    print('1. Login')
    print('2. Register new account')

    decision = input("")
    while decision != '1' and decision != '2':
        print('Please enter 1 or 2')
        decision = input("")

    if decision == '1':
        login()
    else:
        conn = sqlite3.connect('user_database.db')
        register(conn)


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

    # Get user input
    decision = input("")
    while decision != '1' and decision != '2' and decision != '3':
        print('Please enter 1, 2, or 3')
        decision = input("")

    # Route input to proper function
    if decision == '1':
        job_search()
    elif decision == '2':
        find_user()
    else:
        learn_skill()


def job_search():
    print('Under construction')


def find_user():
    print('Under construction')


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


def register(conn):
    # Ensure there are less than 5 registered users
    num_users = num_registered_users()
    if num_users >= 5:
        print("All permitted accounts have been created, please come back later")
        return
    print('==================')
    print('Registration Page')
    print('==================')

    username = input('Enter username: ')
    # Check if username exists
    while username_exists(username):
        print('This username is already taken. Please select another')
        username = input('Enter username: ')

   # print("Here1")
    password = input('Enter password: ')
   # print("Here2")
    while (not any(char.isupper() for char in password) or
            not any(char.isdigit() for char in password) or
            not any(char in '!@#$%^&*()_+' for char in password) or
            len(password) < 8 or len(password) > 12):
        print('Password must contain a capital letter, a digit, a special character, '
              'and be between 8-12 characters in length')
        #print("Here3")
        password = input('Enter password: ')
        #print("Here4")

    # Insert account into database
    db = conn.cursor()
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()


def username_exists(username):
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()

    # Check if user exists in database
    db.execute("SELECT 1 FROM users WHERE username=?", (username,))
    output = db.fetchone()
    print("danieldebug", output)
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


if __name__ == "__main__":
    main()