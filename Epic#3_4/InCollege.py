import sqlite3

# Global vars to keep track of logged-in user
LOGGED_IN_FIRST = ""
LOGGED_IN_LAST = ""


def main():
    # Initialize database connection
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()
    # Create database if it doesn't already exist
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
    # Create a friends table is it doesn't already exist
    db.execute('''CREATE TABLE IF NOT EXISTS friends (
    user1 TEXT,
    user2 TEXT,
    status TEXT,
    PRIMARY KEY(user1, user2),
    FOREIGN KEY(user1) REFERENCES users(username),
    FOREIGN KEY(user2) REFERENCES users(username)
)''')
    
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
    print('5. Useful Links')
    print('6. InCollege Important Links')
    print('7. Exit')

    decision = input("")
    while decision != '1' and decision != '2' and decision != '3' and decision != '4' and decision != '5'\
            and decision != '6':
        if decision == '7':
            break
        print('Please enter 1-7')
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
    elif decision == '4':
        f_name = input("First: ")
        l_name = input("Last: ")
        search_by_name(f_name, l_name)
    elif decision == '5':
        logged_in = False
        useful_links(logged_in, conn)
    elif decision == '6':
        policies()


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
    print('4. Useful Links')
    print('5. InCollege Important Links')
    print('6. Logout')

    # Get user input
    decision = input("")
    while decision != '1' and decision != '2' and decision != '3' and decision != '4' and decision != '5'\
            and decision != '6':
        print('Please enter 1 - 6')
        decision = input("")

    # Route input to proper function
    if decision == '1':
        job_search()
    elif decision == '2':
        find_user()
    elif decision == '3':
        learn_skill()
    elif decision == '4':
        logged_in = True
        conn = sqlite3.connect('user_database.db')
        useful_links(logged_in, conn)
    elif decision == '5':
        policies()
    elif decision == '6':
        # Empty global vars upon logout
        global LOGGED_IN_FIRST, LOGGED_IN_LAST
        LOGGED_IN_FIRST, LOGGED_IN_LAST = "", ""
        return


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
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()

    print("Search by:")
    print("1. First Name")
    print("2. Last Name")
    print("3. Both First and Last Name")
    print("4. University Name")
    print("5. Major")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        search_term = input("Enter First Name: ")
        db.execute("SELECT * FROM users WHERE first_name LIKE ?", ('%' + search_term + '%',))

    elif choice == "2":
        search_term = input("Enter Last Name: ")
        db.execute("SELECT * FROM users WHERE last_name LIKE ?", ('%' + search_term + '%',))

    elif choice == "3":
        f_name = input("Enter First Name: ")
        l_name = input("Enter Last Name: ")
        db.execute("SELECT * FROM users WHERE first_name LIKE ? AND last_name LIKE ?", ('%' + f_name + '%', '%' + l_name + '%',))

    elif choice == "4":
        search_term = input("Enter University Name: ")
        db.execute("SELECT * FROM users WHERE university LIKE ?", ('%' + search_term + '%',))

    elif choice == "5":
        search_term = input("Enter Major: ")
        db.execute("SELECT * FROM users WHERE major LIKE ?", ('%' + search_term + '%',))

    elif choice == "6":
        return

    else:
        print("Invalid choice. Try again.")
        find_user()
        return

    users = db.fetchall()
    conn.close()

    if not users:
        print('No match found in the InCollege system.')
        print('1. Go Back')
        decision = input("")
        while decision != '1':
            decision = input('')
        main()
    else:
        for user in users:
            print(f"Name: {user[2]} {user[3]}, University: {user[8]}, Major: {user[9]}")
        print('1. Go Back')
        decision = input("")
        while decision != '1':
            decision = input('')
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
    # There can be at most 10 student accounts
    num_users = num_registered_users()
    if num_users >= 10:
        print("All permitted accounts have been created, please come back later")
        return
    print('==================')
    print('Registration Page')
    print('==================')

    # Retrieve names
    f_name = input('First name: ')
    l_name = input('Last name: ')
    uni = input('University name: ')
    major = input('Major: ')
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
    db.execute("INSERT INTO users (username, password, first_name, last_name, university, major, email, sms, advertising, language)"
               "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
               (username, password, f_name, l_name, uni, major, True, True, True, 'English'))

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


def about():
    print("In College: Welcome to In College, the world's largest college student network "
          "with many users in many countries and territories worldwide. This is some information "
          "about the history and purpose of the company.")


def useful_links(logged_in, conn):
    print("Useful Links:")
    print("1. General")
    print("2. Browse InCollege")
    print("3. Business Solutions")
    print("4. Directories")
    print('5. Go back')

    choice = input("")
    while choice != '1' and choice != '2' and choice != '3' and choice != '4' and choice != '5':
        choice = input("")

    if choice == "1":
        general_links(logged_in, conn)
    elif choice == "2":
        print("Under construction")
    elif choice == "3":
        print("Under construction")
    elif choice == "4":
        print("Under construction")
    elif choice == '5':
        main()


def general_links(logged_in, conn):
    print("General Links:")
    if not logged_in:
        print("1. Sign Up")
    print("2. Help Center")
    print("3. About")
    print("4. Press")
    print("5. Blog")
    print("6. Careers")
    print("7. Developers")
    print("8. Go Back")

    choice = input("")

    while choice != '1' and choice != '2' and choice != '3' and choice != '4' and choice != '5'\
            and choice != '6' and choice != '7' and choice != '8':
        choice = input("")

    if choice == "1" and not logged_in:
        conn = sqlite3.connect('user_database.db')
        register(conn)
    elif choice == "2":
        print("We're here to help.")
    elif choice == "3":
        about()
    elif choice == "4":
        print("In College Pressroom: Stay on top of the latest news, updates, and reports.")
    elif choice == "5" or choice == "6" or choice == "7":
        print("Under construction")
    elif choice == "8":
        useful_links(logged_in, conn)


def guest_controls():
    # If user is not logged in, they will not have any settings
    if not LOGGED_IN_FIRST:
        print('You must login to access this page')
        print('1. Go back')
        decision = input("")
        while decision != '1':
            decision = input("")
        policies()
        return
    conn = sqlite3.connect("user_database.db")
    db = conn.cursor()
    db.execute("SELECT * FROM users WHERE first_name=? AND last_name=?", (LOGGED_IN_FIRST, LOGGED_IN_LAST))
    result = db.fetchone()
    email, sms, advertising, language = result[4], result[5], result[6], result[7]
    print("Guest Controls")

    print("1. InCollege Email\n"
          "2. SMS\n"
          "3. Targeted Advertising\n"
          "4. Languages\n"
          "5. Go back")
    choice = input("")
    while choice != '1' and choice != '2' and choice != '3' and choice != '4' and choice != '5':
        print("Please enter 1 - 5")
        choice = input("")

    # InCollege Email settings
    if choice == '1':
        if email:
            print('Email is turned on')
            print('1. Turn off')
            print('2. Go back')
            decision = input("")
            while decision != '1' and decision != '2':
                decision = input("")
        else:
            print('Email is turned off')
            print('1. Turn on')
            print('2. Go back')
            decision = input("")
            while decision != '1' and decision != '2':
                decision = input("")

        if decision == '1':
            # Update database
            if email:
                db.execute("UPDATE users SET email=? WHERE first_name=? AND last_name=?",
                           (False, LOGGED_IN_FIRST, LOGGED_IN_LAST))
                print('Success!')
            else:
                db.execute("UPDATE users SET email=? WHERE first_name=? AND last_name=?",
                           (True, LOGGED_IN_FIRST, LOGGED_IN_LAST))
                print('Success!')
        conn.commit()
        conn.close()
        guest_controls()

    # SMS settings
    elif choice == '2':
        if sms:
            print('SMS is turned on')
            print('1. Turn off')
            print('2. Go back')
            decision = input("")
            while decision != '1' and decision != '2':
                decision = input("")
        else:
            print('SMS is turned off')
            print('1. Turn on')
            print('2. Go back')
            decision = input("")
            while decision != '1' and decision != '2':
                decision = input("")

        if decision == '1':
            # Update database
            if sms:
                db.execute("UPDATE users SET sms=? WHERE first_name=? AND last_name=?",
                           (False, LOGGED_IN_FIRST, LOGGED_IN_LAST))
                print('Success!')
            else:
                db.execute("UPDATE users SET sms=? WHERE first_name=? AND last_name=?",
                           (True, LOGGED_IN_FIRST, LOGGED_IN_LAST))
                print('Success!')
        conn.commit()
        conn.close()
        guest_controls()

    # Targeted Advertising settings
    elif choice == '3':
        if advertising:
            print('Targeted Advertising is turned on')
            print('1. Turn off')
            print('2. Go back')
            decision = input("")
            while decision != '1' and decision != '2':
                decision = input("")
        else:
            print('Targeted Advertising is turned off')
            print('1. Turn on')
            print('2. Go back')
            decision = input("")
            while decision != '1' and decision != '2':
                decision = input("")

        if decision == '1':
            # Update database
            if advertising:
                db.execute("UPDATE users SET advertising=? WHERE first_name=? AND last_name=?",
                           (False, LOGGED_IN_FIRST, LOGGED_IN_LAST))
                print('Success!')
            else:
                db.execute("UPDATE users SET advertising=? WHERE first_name=? AND last_name=?",
                           (True, LOGGED_IN_FIRST, LOGGED_IN_LAST))
                print('Success!')
        conn.commit()
        conn.close()
        guest_controls()

    # Language settings
    elif choice == '4':
        if language == 'English':
            print('Language is set to English')
            print('1. Switch to Spanish')
            print('2. Go back')
            decision = input("")
            while decision != '1' and decision != '2':
                decision = input("")
        else:
            print('Language is set to Spanish')
            print('1. Switch to English')
            print('2. Go back')
            decision = input("")
            while decision != '1' and decision != '2':
                decision = input("")

        if decision == '1':
            # Update database
            if language == 'English':
                db.execute("UPDATE users SET language=? WHERE first_name=? AND last_name=?",
                           ('Spanish', LOGGED_IN_FIRST, LOGGED_IN_LAST))
                print('Success!')
            else:
                db.execute("UPDATE users SET language=? WHERE first_name=? AND last_name=?",
                           ('English', LOGGED_IN_FIRST, LOGGED_IN_LAST))
                print('Success!')
        conn.commit()
        conn.close()
        guest_controls()

    elif choice == '5':
        policies()


def policies():
    print("Welcome to the policies section!")
    print("1. A Copyright Notice\n"
          "2. About\n"
          "3. Accessibility\n"
          "4. User Agreement\n"
          "5. Privacy Policy\n"
          "6. Cookie Policy\n"
          "7. Copyright policy\n"
          "8. Brand policy\n"
          "9. Go back")
    choice = input("")
    while choice != '1' and choice != '2' and choice != '3' and choice != '4' and choice != '5'\
            and choice != '6' and choice != '7' and choice != '8' and choice != '9':
        choice = input("")

    if choice == '1':
        print("Copyright Notice")
        print("The software for this tool is open-source."
              " This means that anyone can view the code and submit their changes to it.")
        print('1. Go back')
        decision = input("")
        while decision != '1':
            decision = input("")
        policies()

    elif choice == '2':
        print("About")
        about()
        print('1. Go back')
        decision = input("")
        while decision != '1':
            decision = input("")
        policies()

    elif choice == '3':
        print("Accessibility")
        print("We ensure to make our tool accessible to everyone. Please reach out to us if there is any issue")
        print('1. Go back')
        decision = input("")
        while decision != '1':
            decision = input("")
        policies()

    elif choice == '4':
        print("User Agreement")
        print("This is a legal agreement between you(the licensee) and the licensor. There will be no fee assessed by"
              " the licensor for the product. This policy will be updated regularly.")
        print('1. Go back')
        decision = input("")
        while decision != '1':
            decision = input("")
        policies()

    elif choice == '5':
        print("Privacy Policy")
        print("We strive to make sure your data is handled correctly and in a confidential manner."
              " Please reach out to us if there has been any issues with it.")
        print("1. Guest Controls")
        print("2. Go back")
        decision = input("")
        while decision != '1' and decision != '2':
            decision = input("")
        if decision == '1':
            guest_controls()
        else:
            policies()

    elif choice == '6':
        print("Cookie Policy")
        print("We only store essential cookies to make sure the user is authentic."
              " This is also done to prevent any security vulnerabilites.")
        print('1. Go back')
        decision = input("")
        while decision != '1':
            decision = input("")
        policies()

    elif choice == '7':
        print("Copyright Policy")
        print("We have a copyright policy to make sure our product is not used in the wrong manner.")
        print('1. Go back')
        decision = input("")
        while decision != '1':
            decision = input("")
        policies()

    elif choice == '8':
        print("Brand Policy")
        print("We aim to make sure that each and every process in our software is consistent."
              " This policy is subject to further change")
        print('1. Go back')
        decision = input("")
        while decision != '1':
            decision = input("")
        policies()

    elif choice == '9':
        if not LOGGED_IN_FIRST:
            main()
        else:
            logged_in()  


if __name__ == "__main__":
    main()
