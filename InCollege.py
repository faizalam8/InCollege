import sqlite3


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
        print('Please enter 1, 2, or 3')
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
            print('Please enter 1 to go back')
            decision = input('')
        main()
    else:
        print('They are a part of the InCollege system')
        print('1. Go Back')
        decision = input("")
        while decision != '1':
            print('Please enter 1 to go back')
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
    print('=====')
    job = sqlite3.connect("jobs.db")
    db = job.cursor()
    db.execute('''CREATE TABLE IF NOT EXISTS jobs (title TEXT PRIMARY KEY,description TEXT,employer TEXT,location TEXT,salary TEXT)'''
    job.commit()
    choice = int(input('Would you like to go to the previous page or would you like to post your job? Type 1 to go back and 2 to continue'))
    if(choice == 1):
        print("Going back to the previous page")
        logged_in()
    elif(choice == 2):
        
        #code below helps post a job
        num = input("How many jobs do you want to post?")
        if(num <= 5):
            title = input("Enter the job title:")
            description = input("Enter the job description:")
            employer = input("Enter the employer name:")
            location = input("Enter the job location:")
            salary = string(input("Enter the job salary:"))
        
            #job = sqlite3.connect("jobs.db")
            #db = job.cursor()
            db.execute('''INSERT INTO jobs (title, description, employer, location, salary) VALUES (?, ?, ?, ?, ?)''', (title, description, employer, location, salary))
            job.commit()
            print("Sucess! Your job has been posted!")
            job.close()
        else: 
            print("The number of jobs that can be posted is only upto 5 jobs!")
    else:
        print("Wrong input! Please try again.")
        
def find_user():
    #Option to connect with people 
    choice = int(input('Would you like to connect to people who could help you? Type 1 for yes or 2 for no.'))
    if(choice == 1):
        name = input('Who would you like to search for? Enter their username here:')
        if(username_exists(name)):
            print("Username found!")
        else:
            print("Username not found. Please input another username")

    elif(choice == 2):#option to go back
        choice1 = int(input('Understood. Would you like to go back to the display page? Type 1 for yes and 2 for no'))
        if(choice1 == 1):
            logged_in()
        elif(choice1 == 2):
            print("You will now be exiting the site")
        else:
            print("Wrong input! Please try again!")
    else:
        print("Wrong choice! Please try again!")

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


if __name__ == "__main__":
    main()
