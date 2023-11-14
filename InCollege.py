import sqlite3
from datetime import datetime

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
        user_id TEXT,
        tier TEXT,
        new_msg BOOLEAN,
        register_date TEXT
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

    # Table for messages
    db.execute('''CREATE TABLE IF NOT EXISTS messages (
            to_user TEXT,
            from_user TEXT,
            message TEXT
            )''')

    # Create the connections table
    db.execute('''CREATE TABLE IF NOT EXISTS connections (
        user TEXT,
        username TEXT,
        FOREIGN KEY (user) REFERENCES users (username),
        FOREIGN KEY (username) REFERENCES users (username)
        )''')

    # Table for friend requests
    db.execute('''CREATE TABLE IF NOT EXISTS friend_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_user TEXT,
    to_user TEXT,
    status INTEGER DEFAULT 0,
    FOREIGN KEY (from_user) REFERENCES users(username),
    FOREIGN KEY (to_user) REFERENCES users(username)
    )''')

    # Table for jobs
    db.execute('''CREATE TABLE IF NOT EXISTS jobs (
        title TEXT PRIMARY KEY,
        description TEXT,
        employer TEXT,
        location TEXT,
        salary TEXT,
        firstName TEXT,
        lastName TEXT)''')

    # Table for applications
    db.execute('''CREATE TABLE IF NOT EXISTS applications (
        user TEXT PRIMARY KEY,
        jobTitle TEXT,
        grad_date TEXT,
        start_date TEXT,
        paragraph TEXT,
        FOREIGN KEY (user) REFERENCES users (username),
        FOREIGN KEY (jobTitle) REFERENCES jobs (title))''')

    # Table for saved jobs
    db.execute('''CREATE TABLE IF NOT EXISTS savedJobs (
            user TEXT,
            jobTitle TEXT,
            FOREIGN KEY (user) REFERENCES users (username),
            FOREIGN KEY (jobTitle) REFERENCES jobs (title)
            )''')
    
    db.execute('''CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            message TEXT,
            is_read BOOLEAN DEFAULT 0
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
    while decision != '1' and decision != '2' and decision != '3' and decision != '4' and decision != '5' \
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
        logged_in()
    else:
        print('Incorrect username / password, please try again')
        login()


def logged_in():
    global LOGGED_IN_FIRST, LOGGED_IN_LAST, LOGGED_IN_USER

    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()
    check_new_job_postings(conn, LOGGED_IN_USER)
    check_deleted_jobs(conn, LOGGED_IN_USER)
    check_new_students_join(conn, LOGGED_IN_USER)
    check_lazy_user(conn)
    conn.close()

    # Display page once logged in
    print('==========')
    print('Home Page')
    print('==========')
    print('1. Job Search')
    print('2. User Search')
    print('3. Learn Skill')
    print('4. Create Profile')
    print('5. View Profile')
    print('6. View Friend Profile')
    print('7. Messages')
    print('8. Useful Links')
    print('9. InCollege Important Links')
    print('10. View and Manage Connections')
    print('11. Logout')

    # Get user input
    decision = input("")
    while decision != '1' and decision != '2' and decision != '3' and decision != '4' and decision != '5' \
            and decision != '6' and decision != '7' and decision != '8' and decision != '9' and decision != '10'\
            and decision != '11':
        print('Please enter 1 - 11')
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
        messages()
    elif decision == '8':
        logged_in = True
        conn = sqlite3.connect('user_database.db')
        useful_links(logged_in, conn)
    elif decision == '9':
        policies()
    elif decision == '10':
        view_and_disconnect_connections(LOGGED_IN_FIRST, LOGGED_IN_LAST)
    elif decision == '11':
        # Empty global vars upon logout
        LOGGED_IN_FIRST, LOGGED_IN_LAST = "", ""
        return


def job_search():
    print('=====')
    print('Jobs')
    print('=====')

    # Create new job or search for a job
    print('1. Search for a job')
    print('2. View all jobs')
    print('3. View applied jobs')
    print('4. View non-applied jobs')
    print('5. View saved jobs')
    print('6. Post a job')
    print('7. Delete a job')
    print('8. Go back')
    decision = input("")
    while decision != '1' and decision != '2' and decision != '3' and decision != '4' and decision != '5' \
            and decision != '6' and decision != '7' and decision != '8':
        print('Please enter 1 - 8')
        decision = input("")
    if decision == '1':
        title = input("Title: ")
        search_for_job(title)
    elif decision == '2':
        view_all_jobs()
    elif decision == '3':
        view_applied_jobs()
    elif decision == '4':
        view_non_applied_jobs()
    elif decision == '5':
        view_saved_jobs()
    elif decision == '6':
        post_job()
    elif decision == '7':
        delete_job()
    elif decision == '8':
        logged_in()


def search_for_job(title):
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()
    db.execute("SELECT * FROM jobs WHERE title=?", (title,))
    job_selection = db.fetchone()
    conn.close()

    if job_selection:
        print("The job you searched for does exist")
        print("Here are the details:")
        print("Job title:", job_selection[0])
        print("Description", job_selection[1])
        print("Employer", job_selection[2])
        print("Location", job_selection[3])
        print("Salary:", job_selection[4])
        print('1. Go back')
        decision = input("")
        while decision != "1":
            decision = input("")
        job_search()
    else:
        print("The job you searched for does not exist!")
        print('1. Go Back')
        decision = input("")
        while decision != '1':
            decision = input('')
        job_search()


def delete_job():
    conn = sqlite3.connect("user_database.db")
    db = conn.cursor()
    title = input("Enter the name of the job to be deleted: ")
    db.execute("SELECT * FROM jobs WHERE title=? AND firstName=? AND lastName=?",
               (title, LOGGED_IN_FIRST, LOGGED_IN_LAST))

    result = db.fetchone()

    # If job exists, delete
    if not result:
        print(f'You have no job posting for {title}')
    else:
        job_to_delete = result[0]
        db.execute("DELETE FROM jobs WHERE title=?", (job_to_delete,))
        conn.commit()
    conn.close()


def view_all_jobs():
    job_count = num_jobs()

    conn = sqlite3.connect("user_database.db")
    db = conn.cursor()
    db.execute("SELECT * FROM jobs")
    result = db.fetchall()
    conn.close()

    # If no jobs
    if job_count == 0:
        print('There are currently no jobs available')
        print('1. Go back')
        decision = input('')
        while decision != '1':
            decision = input('')
        job_search()
        return

    # Display all jobs
    for i in range(job_count):
        print(f'\n{i + 1}. {result[i][0]}')
        print('Description:', result[i][1])
        print('Employer:', result[i][2])
        print('Location:', result[i][3])
        print('Salary:', result[i][4])

    print("Select a job for more options or enter 0 to go back")
    choice = int(input(''))
    while choice > job_count:
        choice = int(input(''))
    if choice == 0:
        job_search()
        return

    # Apply for job or save for later
    choice = int(choice) - 1
    selected_title = result[choice][0]
    print(f'You selected {selected_title}')
    print('1. Apply')
    print('2. Save for later')
    print('3. Go back')

    decision = input('')
    while decision != '1' and decision != '2' and decision != '3':
        decision = input('')

    if decision == '1':
        # Check if user has already applied
        conn = sqlite3.connect("user_database.db")
        db = conn.cursor()
        db.execute("SELECT * FROM applications WHERE user=?", (LOGGED_IN_USER,))
        result = db.fetchone()

        # If user has already applied
        if result:
            print('You have already applied to this job')
            print('1. Go back')
            choice = input('')
            while choice != '1':
                choice = input('')
            job_search()
            return

        # Check if user is the owner of the job posting
        db.execute("SELECT * FROM jobs WHERE firstName=? AND lastName=?", (LOGGED_IN_FIRST, LOGGED_IN_LAST))
        result = db.fetchone()
        if result:
            print('You cannot apply to your own job posting')
            print('1. Go back')
            choice = input('')
            while choice != '1':
                choice = input('')
            job_search()
            return

        grad_date = input('Enter grad date (MM/DD/YYYY): ')
        start_date = input('Enter start date (MM/DD/YYYY): ')
        paragraph = input('Why you would be a good fit: ')
        apply_for_job(selected_title, grad_date, start_date, paragraph)

    elif decision == '2':
        save_job(selected_title)

    elif decision == '3':
        job_search()


def view_applied_jobs():
    conn = sqlite3.connect("user_database.db")
    db = conn.cursor()
    db.execute("SELECT jobTitle FROM applications WHERE user=?", (LOGGED_IN_USER,))
    result = db.fetchall()
    conn.close()

    if not result:
        print("You haven't applied to any jobs")
        print('1. Go back')
        choice = input("")
        while choice != '1':
            choice = input("")
        job_search()
        return

    print(f'You have currently applied for {len(result)} jobs:')
    for i in range(len(result)):
        print(f'{i+1}. {result[i][0]}')

    print(f'{len(result)+1}. Go back')
    choice = input("")
    while choice != str(len(result)+1):
        choice = input("")
    job_search()


def view_non_applied_jobs():
    # Retrieve jobs not applied for
    conn = sqlite3.connect("user_database.db")
    db = conn.cursor()
    db.execute('''
        SELECT j.title, j.description, j.employer, j.location, j.salary 
        FROM jobs j
        LEFT JOIN applications a 
        ON j.title = a.jobTitle AND a.user = ? 
        WHERE a.jobTitle IS NULL
        ''', (LOGGED_IN_USER,))
    result = db.fetchall()
    conn.close()

    if not result:
        print('You have applied to all job postings')
        print('1. Go back')
        choice = input("")
        while choice != '1':
            choice = input("")
        job_search()
        return

    for i in range(len(result)):
        print(f'\n{i + 1}. {result[i][0]}')
        print('Description:', result[i][1])
        print('Employer:', result[i][2])
        print('Location:', result[i][3])
        print('Salary:', result[i][4])

    print('Enter 0 to go back')
    choice = input('')
    while choice != '0':
        choice = input('')
    job_search()


def view_saved_jobs():
    # Retrieve and display saved jobs
    conn = sqlite3.connect("user_database.db")
    db = conn.cursor()
    db.execute("SELECT jobTitle FROM savedJobs WHERE user=?", (LOGGED_IN_USER,))
    result = db.fetchall()
    conn.close()

    if not result:
        print("You haven't saved any jobs")
        print('1. Go back')
        choice = input("")
        while choice != '1':
            choice = input("")
        job_search()
        return

    print('You have saved the following jobs:')
    for i in range(len(result)):
        print(f'{i+1}. {result[i][0]}')
    print(f'{len(result)+1}. Go back')

    print('Selecting a job will unsave it')
    choice = input("")
    while int(choice) > len(result)+1 or int(choice) < 0:
        choice = input("")

    if choice == str(len(result)+1):
        job_search()
        return
    else:
        selected_job = int(choice) - 1
        selected_job_title = result[selected_job][0]
        unsave_job(selected_job_title)


def unsave_job(title):
    conn = sqlite3.connect("user_database.db")
    db = conn.cursor()
    db.execute('''DELETE FROM savedJobs WHERE user=? AND jobTitle=?''', (LOGGED_IN_USER, title))
    conn.commit()
    conn.close()
    print('Job removed from saved list!')


def save_job(title):
    conn = sqlite3.connect("user_database.db")
    db = conn.cursor()
    db.execute('''INSERT INTO savedJobs (user, jobTitle) VALUES (?, ?)''', (LOGGED_IN_USER, title))
    conn.commit()
    conn.close()
    print('Job saved!')


def apply_for_job(title, grad_date, start_date, paragraph):
    conn = sqlite3.connect("user_database.db")
    db = conn.cursor()
    db.execute("INSERT INTO applications (user, jobTitle, grad_date, start_date, paragraph) VALUES (?, ?, ?, ?, ?)",
               (LOGGED_IN_USER, title, grad_date, start_date, paragraph))
    conn.commit()
    conn.close()
    print('Application sent!')


def post_job():
    if num_jobs() >= 10:
        print('10 jobs have already been posted')
        print('1. Go back')
        decision = input("")
        while decision != "1":
            decision = input("")
        job_search()
        return

    title = input("Job title: ")
    description = input("Description: ")
    employer = input("Employer: ")
    location = input("Location: ")
    salary = input("Salary: ")

    conn = sqlite3.connect("user_database.db")
    db = conn.cursor()
    db.execute('''INSERT INTO jobs (title, description, employer, location, salary, firstName, lastName)
     VALUES (?, ?, ?, ?, ?, ?, ?)''', (title, description, employer, location, salary, LOGGED_IN_FIRST, LOGGED_IN_LAST))
    conn.commit()
    conn.close()
    print("Success! Your job has been posted")


def messages():
    # Retrieve logged in user
    conn = sqlite3.connect("user_database.db")
    db = conn.cursor()
    db.execute("SELECT * FROM users WHERE first_name = ? AND last_name = ?", (LOGGED_IN_FIRST, LOGGED_IN_LAST))
    result = db.fetchone()

    username = result[0]
    notif = result[14]
    tier = result[13]

    # Display any new user message notifications
    if notif:
        print('You have a new message!')
        db.execute("UPDATE users SET new_msg=? WHERE username=?", (False, LOGGED_IN_USER))
        conn.commit()
        conn.close()

    # Do this for all standard users
    if tier == 'standard':
        print('1. Inbox')
        print('2. Send a message')
        print('3. Go back')
        choice = input('')
        while choice != '1' and choice != '2' and choice != '3':
            choice = input('')

        if choice == '1':
            inbox(username)
        elif choice == '2':
            send_message(username)
        elif choice == '3':
            logged_in()

    # Do this for all plus users
    elif tier == 'plus':
        print('1. Inbox')
        print('2. Send a message')
        print('3. Go back')

        choice = input('')
        while choice != '1' and choice != '2' and choice != '3':
            choice = input('')

        if choice == '1':
            inbox(username)
        elif choice == '2':
            send_message(None)
        elif choice == '3':
            logged_in()


def inbox(username):
    conn = sqlite3.connect("user_database.db")
    db = conn.cursor()
    db.execute("SELECT * FROM messages WHERE to_user=?", (username,))
    result = db.fetchall()

    # If inbox is empty
    if not result:
        print('You have no messages in your inbox')
        print('1. Go back')
        choice = input('')
        while choice != '1':
            choice = input('')
        messages()
    else:
        print('Select a message to open or enter 0 to go back: ')
        for i in range(len(result)):
            from_user = result[i][1]
            print(f'{i+1}. {from_user}')

        choice = int(input(''))
        while choice < 0 or choice > len(result):
            choice = int(input(''))

        # If user chooses to go back
        if choice == 0:
            messages()
            return

        # Display selected message
        print(f'From {result[choice-1][1]}:')
        print(result[choice-1][2])

        print('\n1. Reply to message')
        print('2. Delete message')
        print('3. Go back')
        decision = input('')
        while decision != '1' and decision != '2' and decision != '3':
            decision = input('')

        # Send message
        if decision == '1':
            message_to_send = input('Enter message: ')
            db.execute("INSERT INTO messages (to_user, from_user, message) VALUES (?, ?, ?)",
                       (result[choice - 1][1], LOGGED_IN_USER, message_to_send))
            conn.commit()
            print('Message has been sent!')

        # Delete message
        elif decision == '2':
            db.execute("DELETE FROM messages WHERE to_user=? AND from_user=? AND message=?",
                       (LOGGED_IN_USER, result[choice - 1][1], result[choice - 1][2]))
            conn.commit()
            print('Message deleted!')
        elif decision == '3':
            messages()

    conn.close()


def send_message(username):
    # if None value is passed into function, we have a plus user. else, standard user
    if not username:
        conn = sqlite3.connect('user_database.db')
        db = conn.cursor()
        db.execute("SELECT username FROM users WHERE username != ?", (LOGGED_IN_USER,))
        all_users = db.fetchall()

        # If no other users exist
        if not all_users:
            print('There are no other existing users')
            print('1. Go back')
            choice = input('')
            while choice != '1':
                choice = input('')
            messages()
            return

        print('Select a user to send a message or enter 0 to go back')
        for i in range(len(all_users)):
            print(f'{i+1}. {all_users[i][0]}')

        choice = int(input(''))
        while choice < 0 or choice > len(all_users):
            choice = int(input(''))

        # If user chooses to go back
        if choice == 0:
            messages()
            return

        recipient = all_users[choice-1][0]

        message_to_send = input('Enter message: ')
        db.execute("INSERT INTO messages (to_user, from_user, message) VALUES (?, ?, ?)",
                   (recipient, LOGGED_IN_USER, message_to_send))
        conn.commit()
        db.execute("UPDATE users SET new_msg=? WHERE username=?", (True, recipient))
        conn.commit()
        conn.close()
        print('Message has been sent!')

    else:
        conn = sqlite3.connect('user_database.db')
        db = conn.cursor()
        db.execute("SELECT username FROM connections WHERE user = ?", (LOGGED_IN_USER,))
        all_friends = db.fetchall()

        # If user has no connections
        if not all_friends:
            print('You have no connections to send messages to')
            print('1. Go back')
            choice = input('')
            while choice != '1':
                choice = input('')
            messages()
            return

        print('Select a user to send a message or enter 0 to go back')
        for i in range(len(all_friends)):
            print(f'{i + 1}. {all_friends[i][0]}')

        choice = int(input(''))
        while choice < 0 or choice > len(all_friends):
            choice = int(input(''))

        # If user chooses to go back
        if choice == 0:
            messages()
            return

        recipient = all_friends[choice-1][0]
        message_to_send = input('Enter message: ')

        db.execute("INSERT INTO messages (to_user, from_user, message) VALUES (?, ?, ?)",
                   (recipient, LOGGED_IN_USER, message_to_send))
        conn.commit()
        db.execute("UPDATE users SET new_msg=? WHERE username=?", (True, recipient))
        conn.commit()
        conn.close()
        print('Message has been sent!')


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
        db.execute("SELECT * FROM users WHERE first_name LIKE ? AND last_name LIKE ?",
                   ('%' + f_name + '%', '%' + l_name + '%',))

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
    while decision != '1' and decision != '2' and decision != '3' and decision != '4' and decision != '5' \
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
    tier = input('Select tier (standard/plus): ')
    while tier.lower() != 'standard' and tier.lower() != 'plus':
        tier = input('')
    tier = tier.lower()

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
               "advertising, language, user_id, tier, new_msg, register_date)"
               "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
               (username, password, f_name, l_name, uni, major, True, True, True, 'English',
                f"{f_name} {l_name}", tier, False, datetime.now().strftime("%Y-%m-%d")))

    conn.commit()
    notify_new_user(conn, username)
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
        user_id = LOGGED_IN_USER

        conn = sqlite3.connect('user_database.db')
        db = conn.cursor()
        db.execute("UPDATE users SET title=?, major=?, university=?, about=? WHERE user_id=?",
                   (profile_data['title'], profile_data['major'], profile_data['university'],
                    profile_data['about'], user_id))
        conn.commit()

        # User can enter up to 3 experiences
        for _ in range(3):
            title = input('Enter experience title (or enter Q to finish): ')
            print('YOUR TITLE INPUT:', title)
            if title.lower() == 'q':
                break
            employer = input('Enter employer: ')
            date_started = input('Enter date started: ')
            date_ended = input('Enter date ended: ')
            location = input('Enter location: ')
            description = input('Enter description: ')

            db.execute(
                "INSERT INTO experiences (user_id, title, employer, date_started, date_ended, location, description) "
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
    conn = sqlite3.connect("user_database.db")
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

    while choice != '1' and choice != '2' and choice != '3' and choice != '4' and choice != '5' \
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
    while choice != '1' and choice != '2' and choice != '3' and choice != '4' and choice != '5' \
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
              " This is also done to prevent any security vulnerabilities.")
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
    print('Friend request accepted!')


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
            logged_in()
            return

        actual_choice = int(choice) - 1

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
    while decision != '1' and decision != '2' and decision != '3' and decision != str(len(connections) + 1) \
            and decision != str(len(connections) + 2) and decision != str(len(connections) + 3) \
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

    db.execute("SELECT first_name, last_name, title, major, university, about FROM users WHERE username=?",
               (logged_in_user,))
    profile_data = db.fetchone()

    db.execute('SELECT * FROM experiences WHERE user_id=?', (logged_in_user,))
    experiences_data = db.fetchone()
    print(experiences_data)
    conn.close()

    if profile_data:
        first_name, last_name, title, major, university, about = profile_data
        print(f"User Profile for {first_name} {last_name}:")
        print(f"Title: {title}")
        print(f"Major: {major}")
        print(f"University: {university}")
        print(f"About: {about}")
        print('1. Go back')
        choice = input('')
        while choice != '1':
            choice = input('')
        logged_in()
        return
    else:
        print("Profile not found.")


def view_friends_profile(logged_in_user):
    conn = sqlite3.connect('user_database.db')
    db = conn.cursor()

    db.execute("SELECT username FROM connections WHERE user=?", (logged_in_user,))
    friends = db.fetchall()

    if not friends:
        print("You don't have any friends to view their profiles.")
        conn.close()
        print('1. Go back')
        choice = input('')
        while choice != '1':
            choice = input('')
        logged_in()
        return

    print("Your Friends:")
    for idx, friend in enumerate(friends, start=1):
        print(f"{idx}. {friend[0]}")

    selection = input("Enter the number of the friend whose profile you want to view (0 to go back): ")

    try:
        selection = int(selection)
    except ValueError:
        print("Invalid input. Please enter a number.")
        selection = input('')
        conn.close()
        return

    if 0 < selection <= len(friends):
        selected_friend = friends[selection - 1][0]

        db.execute("SELECT title, major, university, about FROM users WHERE username=?", (selected_friend,))
        friend_profile = db.fetchone()
        conn.close()

        if friend_profile:
            title, major, university, about = friend_profile
            print(f"Profile of {selected_friend}:")
            print(f"Title: {title}")
            print(f"Major: {major}")
            print(f"University: {university}")
            print(f"About: {about}")
            print('1. Go back')
            choice = input('')
            while choice != '1':
                choice = input('')
            logged_in()
            return
        else:
            print(f"{selected_friend} does not have a profile.")
    elif selection == 0:
        conn.close()
        logged_in()
    else:
        print("Invalid selection. Please select a valid friend.")


def notify_new_user(conn, new_username):
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username != ?", (new_username,))
    existing_users = cursor.fetchall()
    for user in existing_users:
        user_id = user[0]
        message = f"{new_username} has joined InCollege"
        cursor.execute("INSERT INTO notifications (user_id, message) VALUES (?, ?)", (user_id, message))
        conn.commit()


def check_new_job_postings(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM jobs WHERE title NOT IN (SELECT message FROM notifications WHERE user_id = ?) LIMIT 1", (user_id,))
    result = cursor.fetchone()
    if result:
        job_title = result[0]
        print(f"A new job has been posted: {job_title}")


def check_deleted_jobs(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1
        FROM applications AS a
        WHERE NOT EXISTS (
            SELECT 1
            FROM jobs AS j
            WHERE j.title = a.jobTitle
        )
        AND a.user = ?
        LIMIT 1
    """, (user_id,))
    
    result = cursor.fetchone()
    if result:
        print("A job that you applied for has been deleted.")


def check_new_students_join(conn, user_id):
    cursor = conn.cursor()
    query = "SELECT message FROM notifications WHERE user_id = ? AND message LIKE ?"
    cursor.execute(query, (user_id, "%has joined InCollege%"))
    results = cursor.fetchall()
    if results:
        for result in results:
            message = result[0]
            print(message)

    # Drop old notifications for current user
    cursor.execute("DELETE FROM notifications WHERE user_id = ?", (user_id,))
    conn.commit()


def check_lazy_user(conn):
    db = conn.cursor()
    db.execute("SELECT jobTitle FROM applications WHERE user=?", (LOGGED_IN_USER,))
    jobs_applied = db.fetchall()

    result = db.execute("SELECT register_date FROM users WHERE username=?", (LOGGED_IN_USER,))
    register_date = result.fetchone()[0]
    register_date = datetime.strptime(register_date, "%Y-%m-%d")

    if jobs_applied == 0 and (datetime.now() - register_date).days >= 7:
        print("Remember - you're going to want to have a job when you graduate."
              "Make sure that you start to apply for jobs today!")


if __name__ == "__main__":
    main()
