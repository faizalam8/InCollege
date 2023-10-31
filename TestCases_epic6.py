import pytest
from unittest.mock import patch, MagicMock
import sqlite3
from InCollege import post_job, delete_job

TEST_DB_NAME = "test_user_database.db"

@pytest.fixture(scope="module")
def setup_test_database():
    conn = sqlite3.connect(TEST_DB_NAME)
    cur = conn.cursor()
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        employer TEXT,
        location TEXT,
        salary REAL,
        firstName TEXT,
        lastName TEXT
    )
    ''')
    
    yield conn, cur
    conn.close()

def test_delete_job_job_not_found(capsys, setup_test_database):
    conn, cur = setup_test_database
    with patch('InCollege.LOGGED_IN_FIRST', 'John'), \
         patch('InCollege.LOGGED_IN_LAST', 'Doe'), \
         patch('InCollege.LOGGED_IN_USER', 'johndoe'), \
         patch('InCollege.sqlite3.connect', return_value=conn), \
         patch('InCollege.sqlite3.Cursor', return_value=cur), \
         patch('builtins.input', side_effect=["Job Title"]):
        delete_job()
        captured = capsys.readouterr()
        captured_output = captured.out
        expected_output = "You have no job posting for Job Title"
        assert expected_output in captured_output

if __name__ == '__main__':
    pytest.main()