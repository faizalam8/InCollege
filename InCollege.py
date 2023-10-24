import sqlite3

# Global vars to keep track of logged-in user
LOGGED_IN_FIRST = ""
LOGGED_IN_LAST = ""
LOGGED_IN_USER = ""


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
    major TEXT,
    title TEXT,
    about TEXT,
    user_id TEXT 
    )''')

    # Table for student experiences 
    db.execute('''CREATE TABLE IF NOT EXISTS experiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    title TEXT,
    employer TEXT,
    date_started TEXT,
    date_ended TEXT,
    location TEXT,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(username)
)''')

    # Table for student education
    db.execute('''CREATE TABLE IF NOT EXISTS educations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    school_name TEXT,
    degree TEXT,
    years_attended TEXT,
    FOREIGN KEY (user_id) REFERENCES users(username)
)''')

    # Create the connections table
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
    global LOGGED_IN_USER
    LOGGED_IN_USER = username

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

        # Display any pending friend requests
        #conn = sqlite3.connect('users_database.db')
        #db = conn.cursor()
        #db.execute("SELECT * FROM friend_requests WHERE to_user=?", (username,))
        #requests = db.fetchall()
        #conn.close()
        #print(requests)
        logged_in()
    else:
        print('Incorrect username / password, please try again')
        login()


def logged_in():
    global LOGGED_IN_FIRST, LOGGED_IN_LAST, LOGGED_IN_USER

    # Display page once logged in
    print('==========')
    print('Home Page')
    print('==========')
    print('1. Job Search')
    print('2. User Search')
    print('3. Learn Skill')
    print('4. Create Profile')  # Added option for profile creation/update
    print('5. View Profile') # Added option to view profile
    print('6. View Friend Profile') # Added option to view friend profile
    print('7. Useful Links')
    print('8. InCollege Important Links')
    print('9. View and Manage Connections')
    print('10. Logout')

    # Get user input
    decision = input("")
    while decision != '1' and decision != '2' and decision != '3' and decision != '4' and decision != '5' \
            and decision != '6' and decision != '7' and decision != '8':
        print('Please enter 1 - 8')
        decision = input("")

    # Route input to proper function
    if decision == '1':
        job_search()
    elif decision == '2':
        find_user()
    elif decision == '3':
        learn_skill()
    elif decision == '4':
        create_profile()  
    elif decision == '5':
        view_own_profile(LOGGED_IN_USER)
    elif decision == '6':
        view_friends_profile(LOGGED_IN_USER)
    elif decision == '7':
        logged_in = True
        conn = sqlite3.connect('user_database.db')
        useful_links(logged_in, conn)
    elif decision == '8':
        policies()
    elif decision == '9':
        view_and_disconnect_connections(LOGGED_IN_FIRST, LOGGED_IN_LAST)
    elif decision == '10':
        # Empty global vars upon logout
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
        return

    print('1. Go back')
    decision = input("")
    while decision != "1":
        decision = input("")
    learn_skill()


def register(conn):
    # Ensure there are less than 5 registered users
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
    db.execute("INSERT INTO users (username, password, first_name, last_name, university, major, email, sms,"
               "advertising, language, user_id)"
               "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
               (username, password, f_name, l_name, uni, major, True, True, True, 'English',
                f"{f_name} {l_name}"))

    conn.commit()
    conn.close()

def create_profile():
    global LOGGED_IN_FIRST, LOGGED_IN_LAST
    if LOGGED_IN_FIRST and LOGGED_IN_LAST:
        # TO DO: Have a separate option for updating profile?
        print('Create Your Profile.')

        profile_data = {
            'title': '',
            'major': '',
            'university': '',
            'about': ''
        }

        profile_data['title'] = input('Enter title: ')
        profile_data['major'] = input('Enter major: ').title()
        profile_data['university'] = input('Enter university name: ').title()
        profile_data['about'] = input('Enter about paragraph: ')

        # Construct user_id
        user_id = f"{LOGGED_IN_FIRST} {LOGGED_IN_LAST}"

        conn = sqlite3.connect('user_database.db')
        db = conn.cursor()
        db.execute("UPDATE users SET title=?, major=?, university=?, about=? WHERE user_id=?",
                   (profile_data['title'], profile_data['major'], profile_data['university'],
                    profile_data['about'], user_id))
        conn.commit()

        # User can enter up to 3 experiences
        for _ in range(3):
            title = input('Enter experience title (or leave empty to finish): ')
            if not title:
                break
            employer = input('Enter employer: ')
            date_started = input('Enter date started: ')
            date_ended = input('Enter date ended: ')
            location = input('Enter location: ')
            description = input('Enter description: ')

            db.execute("INSERT INTO experiences (user_id, title, employer, date_started, date_ended, location, description) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (user_id, title, employer, date_started, date_ended, location, description))
            conn.commit()

        while True:
            school_name = input('Enter school name: ')
            degree = input('Enter degree: ')
            years_attended = input('Enter years attended: ')

            db.execute("INSERT INTO educations (user_id, school_name, degree, years_attended) "
                       "VALUES (?, ?, ?, ?)",
                       (user_id, school_name, degree, years_attended))
            conn.commit()

            another_education = input('Do you want to add another education entry? (yes/no): ').lower()
            if another_education != 'yes':
                break

        conn.close()

        print('Profile created/updated successfully!')
    else:
        print('You must log in before creating/updating your profile.')


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


def add_connection(logged_in_first, logged_in_last):
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()

    # Retrieve username of logged-in user
    db.execute("SELECT username FROM users WHERE first_name = ? AND last_name = ?", (logged_in_first, logged_in_last))
    logged_in_username = db.fetchone()[0]

    # Retrieve a list of available users to choose from
    db.execute("SELECT username FROM users WHERE username != ?",
               (logged_in_username,))
    available_users = db.fetchall()

    conn.close()

    if not available_users:
        print("There are no available users to add as connections.")
        print('1. Go back')
        decision = input("")
        while decision != '1':
            decision = input("")
        logged_in()
        return

    print("Available Users:")
    for i, user in enumerate(available_users, start=1):
        print(f"{i}. {user[0]}")

    print(f"{len(available_users) + 1}. Go back")

    decision = input("Enter the number of the user you want to add as a connection: ")
    while not decision.isdigit() or int(decision) < 1 or int(decision) > len(available_users) + 1:
        decision = input("Please enter a valid option: ")

    if int(decision) == len(available_users) + 1:
        logged_in()
        return

    selected_user = available_users[int(decision) - 1][0]

    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()

    # Check if a friend request has already been sent to the selected user
    db.execute("SELECT 1 FROM friend_requests WHERE from_user=? AND to_user=? AND status=0",
               (f"{logged_in_first} {logged_in_last}", selected_user))
    existing_request = db.fetchone()

    if existing_request:
        conn.close()
        print(f"A friend request has already been sent to {selected_user}.")
        print('1. Go back')
        decision = input("")
        while decision != '1':
            decision = input("")
        logged_in()
        return

    # Send friend request to the selected user
    db.execute("INSERT INTO friend_requests (from_user, to_user) VALUES (?, ?)",
               (f"{logged_in_first} {logged_in_last}", selected_user))
    conn.commit()
    conn.close()

    print(f"Friend request sent to {selected_user}.")
    print('1. Go back')
    decision = input("")
    while decision != '1':
        decision = input("")
    logged_in()


def disconnect_from_connection(logged_in_username):
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()

    # Retrieve connections for the logged-in user
    db.execute("SELECT username FROM connections WHERE user=? AND username IN (SELECT username FROM users)",
               (logged_in_username,))
    connections = db.fetchall()

    conn.close()

    if not connections:
        print("You have no connections to disconnect from.")
        print('1. Go back')
        decision = input("")
        while decision != '1':
            decision = input("")
        logged_in()
        return

    print("Select a user to disconnect from:")
    for i, connection in enumerate(connections, start=1):
        print(f"{i}. {connection[0]}")

    print(f"{len(connections) + 1}. Go back")

    decision = input("")
    while not (decision.isdigit() and 1 <= int(decision) <= len(connections) + 1):
        decision = input("Invalid input. Please enter a valid option: ")

    if int(decision) == len(connections) + 1:
        logged_in()
    else:
        # Disconnect the selected connection
        selected_connection = connections[int(decision) - 1][0]
        confirm = input(f"Are you sure you want to disconnect from {selected_connection}? (yes/no): ").strip().lower()

        if confirm == 'yes':
            conn = sqlite3.connect('user_database.db')
            db = conn.cursor()

            # Delete the connection
            db.execute("DELETE FROM connections WHERE user=? AND username=?",
                       (logged_in_username, selected_connection))
            db.execute("DELETE FROM connections WHERE user=? AND username=?",
                       (selected_connection, logged_in_username))
            conn.commit()
            conn.close()

            print(f"You have successfully disconnected from {selected_connection}.")
            print('1. Go back')
            decision = input("")
            while decision != '1':
                decision = input("")
            logged_in()
        else:
            disconnect_from_connection(logged_in_username)


def accept_friend_request(new_friend_first, new_friend_last, to_user):
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()

    # Retrieve username for new friend
    db.execute("SELECT username FROM users WHERE first_name = ? AND last_name = ?", (new_friend_first, new_friend_last))
    new_friend_username = db.fetchone()[0]

    # Remove the friend request entry
    db.execute("DELETE FROM friend_requests WHERE to_user=? AND from_user=? AND status=0",
               (to_user, f"{new_friend_first} {new_friend_last}"))

    # Add both users as connections
    db.execute("INSERT INTO connections (user, username) VALUES (?, ?)", (new_friend_username, to_user))
    db.execute("INSERT INTO connections (user, username) VALUES (?, ?)", (to_user, new_friend_username))

    conn.commit()
    conn.close()


def view_and_accept_friend_requests(logged_in_first, logged_in_last):
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()

    # Retrieve logged in username
    db.execute("SELECT username FROM users WHERE first_name = ? AND last_name = ?", (logged_in_first, logged_in_last))
    logged_in_username = db.fetchone()

    # Retrieve pending friend requests for the logged-in user using their first and last names
    db.execute("SELECT from_user FROM friend_requests WHERE to_user=? AND status=0",
               (f"{logged_in_username[0]}",))

    pending_requests = db.fetchall()
    conn.close()

    if not pending_requests:
        print(f"You, {logged_in_first} {logged_in_last}, have no pending friend requests.")
        input("Press Enter to go back.")
    else:
        print("Pending Friend Requests:")
        for i, request in enumerate(pending_requests, start=1):
            print(f"{i}. {request[0]}")

        choice = input("Enter the number of the request you want to accept (or '0' to go back): ")
        while int(choice) > len(pending_requests):
            choice = input("")
        if choice == '0':
            return

        actual_choice = int(choice)-1

        # Pull first and last name of new friend
        new_friend_full = pending_requests[actual_choice][0].split()
        new_friend_first = new_friend_full[0]
        new_friend_last = new_friend_full[1]

        conn = sqlite3.connect('user_database.db')
        db = conn.cursor()
        db.execute("UPDATE friend_requests SET status=1 WHERE from_user=? AND to_user=?",
                   (f"{logged_in_first, logged_in_last}", logged_in_username[0]))
        conn.commit()
        conn.close()
        accept_friend_request(new_friend_first, new_friend_last, logged_in_username[0])


def view_and_disconnect_connections(logged_in_first, logged_in_last):
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()

    # Retrieve logged-in user's username
    db.execute("SELECT username FROM users WHERE first_name = ? AND last_name = ?", (logged_in_first, logged_in_last))
    logged_in_username = db.fetchone()[0]
    # Retrieve connections for the logged-in user
    db.execute("SELECT username FROM connections WHERE user=?", (logged_in_username,))
    connections = db.fetchall()

    # Check for pending friend requests
    db.execute("SELECT from_user FROM friend_requests WHERE to_user=?", (f"{logged_in_first} {logged_in_last}",))
    pending_requests = db.fetchall()

    conn.close()
    else_statement = False

    if not connections:
        print("You have no connections.")
    else:
        print("Your Connections:")
        for i, connection in enumerate(connections, start=1):
            print(f"{i}. {connection[0]}")
        print('================')
    if not connections and not pending_requests:
        print('1. Add a connection')
        print('2. View and Accept Friend Requests')
        print('3. Go back')
    elif not connections:
        print('1. Add a connection')
        print('2. View and Accept Friend Requests')
        print(f"{len(connections) + 3}. Go back")
    else:
        print(f"{len(connections) + 1}. Add a connection")
        print(f"{len(connections) + 2}. Delete a connection")
        print(f"{len(connections) + 3}. View and Accept Friend Requests")
        print(f"{len(connections) + 4}. Go back")
        else_statement = True

    decision = input("")
    while decision != '1' and decision != '2' and decision != '3' and decision != str(len(connections) + 1)\
            and decision != str(len(connections) + 2) and decision != str(len(connections) + 3)\
            and decision != str(len(connections) + 4):
        decision = input("")

    if decision == '1' and not else_statement:
        add_connection(logged_in_first, logged_in_last)
    elif decision == '2' and not else_statement:
        view_and_accept_friend_requests(logged_in_first, logged_in_last)
    elif decision == '3' and not else_statement:
        logged_in()
    elif decision == str(len(connections) + 1):
        add_connection(logged_in_first, logged_in_last)
    elif decision == str(len(connections) + 2):
        disconnect_from_connection(logged_in_username)
    elif decision == str(len(connections) + 3):
        view_and_accept_friend_requests(logged_in_first, logged_in_last)
    elif decision == str(len(connections) + 4):
        logged_in()


def view_own_profile(logged_in_user):
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()

    db.execute("SELECT first_name, last_name, title, major, university, about FROM users WHERE username=?", (logged_in_user,))
    profile_data = db.fetchone()

    if profile_data:
        first_name, last_name, title, major, university, about = profile_data
        print(f"User Profile for {first_name} {last_name}:")
        print(f"Title: {title}")
        print(f"Major: {major}")
        print(f"University: {university}")
        print(f"About: {about}")

        conn.close()
        return profile_data
    else:
        print("Profile not found.")
        conn.close()
        return None


def view_friends_profile(logged_in_user):
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()

    db.execute("SELECT username FROM connections WHERE user=?", (logged_in_user,))
    friends = db.fetchall()

    if not friends:
        print("You don't have any friends to view their profiles.")
        conn.close()
        return
    
    print("Your Friends:")
    for idx, friend in enumerate(friends, start=1):
        print(f"{idx}. {friend[0]}")

    selection = input("Enter the number of the friend whose profile you want to view (0 to go back): ")

    try:
        selection = int(selection)
    except ValueError:
        print("Invalid input. Please enter a number.")
        conn.close()
        return
    
    if 0 < selection <= len(friends):
        selected_friend = friends[selection - 1][0]

        db.execute("SELECT title, major, university, about FROM users WHERE username=?", (selected_friend,))
        friend_profile = db.fetchone()

        if friend_profile:
            title, major, university, about = friend_profile[0]
            print(f"Profile of {selected_friend}:")
            print(f"Title: {title}")
            print(f"Major: {major}")
            print(f"University: {university}")
            print(f"About: {about}")
        else:
            print(f"{selected_friend} does not have a profile.")
    elif selection == 0:
        pass
    else:
        print("Invalid selection. Please select a valid friend.")

    conn.close()

if __name__ == "__main__":
    main()
