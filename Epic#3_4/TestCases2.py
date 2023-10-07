# Epic 2 Tests
import InCollege
import pytest
import sqlite3
from unittest.mock import ANY
from unittest.mock import patch, Mock, MagicMock


@pytest.fixture
def conn():
    mock_conn = MagicMock()
    return mock_conn

# Test that the initial screen pops up
def test_initial_page_print(conn):
    with patch('InCollege.input', return_value='7'):
        # Mock database connection 
        with patch('InCollege.sqlite3.connect', return_value=MagicMock()):
            with patch('builtins.print') as mock_print:
                InCollege.main()
                
                # check the lines we expect to be printed
                lines = [
                        '=========================================================================',
                        'Welcome to InCollege! Would you like to log in or register a new account?',
                        '=========================================================================',

                        "SUCCESS STORY: I've been using InCollege for only three months and have managed to land "
                        "two Software Engineering roles! This site has helped me obtain the necessary skills to "
                        "apply, interview, and succeed in the industry.",
                    '1. Login',
                    '2. Register new account',
                    '3. Play video',
                    '4. Search by name',
                    '5. Useful Links',
                    '6. InCollege Important Links',
                    '7. Exit'
                ]
                
                for line in lines:
                    mock_print.assert_any_call(line)

# Check the new enhanced registration 
def test_prompt_for_first_and_last_name():
    # Mocking user input
    user_inputs = ['Johnny', 'Depp', 'uni', 'major', 'johndoe', 'Password123!']
    
    with patch('builtins.input', side_effect=user_inputs) as mock_input, \
         patch('InCollege.username_exists', return_value=False), \
         patch('InCollege.num_registered_users', return_value=0):

        # Mocking database connection and cursor
        mock_conn = Mock()
        mock_cursor = mock_conn.cursor.return_value
        
        InCollege.register(mock_conn)
        
        # Check if user was prompted for first and last name
        assert mock_input.call_count == 6  # 4 because we're simulating 4 inputs
        assert mock_input.call_args_list[0][0][0] == 'First name: '
        assert mock_input.call_args_list[1][0][0] == 'Last name: '
        
        # Check if the right details were inserted to the database
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO users (username, password, first_name, last_name, university, major, email, sms, advertising, language)"
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('johndoe', 'Password123!', 'Johnny', 'Depp', ANY, ANY, True, True, True, 'English')
        )

# Test the insertion of a new job
def test_insert_new_job(conn, capsys):
    # Setup the global logged-in user's name
    global LOGGED_IN_FIRST, LOGGED_IN_LAST
    LOGGED_IN_FIRST = "John"
    LOGGED_IN_LAST = "Doe"

    # Mock user input
    job_inputs = ["Software Engineer", "Develop software", "Tech", "TX", "$100,000", "", ""]
    with patch('InCollege.input', side_effect=job_inputs):
        # Mock database connection 
        with patch('InCollege.sqlite3.connect', return_value=conn):
            # Mock the response that there are 4 jobs already posted
            conn.cursor().fetchone.return_value = [4] 

            # Execute post job function
            InCollege.post_job()

            # Check if the job was inserted with the right details
            out, err = capsys.readouterr()
            assert out == "Success! Your job has been posted\n"

  




