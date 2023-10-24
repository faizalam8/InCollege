import sqlite3
from unittest.mock import patch
import pytest
from InCollege import view_own_profile
from InCollege import view_friends_profile
import textwrap

@patch('sqlite3.connect')
def test_view_own_profile(mock_connect, capsys):
    #Defines a custom cursor that returns data
    class CustomCursor:
        def execute(self, query, params):
            return

        def fetchone(self):
            return ("John", "Doe", "Engineer", "Computer Science", "Example University", "About John Doe")

    #Mocks the database connection
    mock_cursor = CustomCursor()
    mock_connect.return_value.cursor.return_value = mock_cursor

    #Runs the function
    result = view_own_profile("john_doe")
    captured = capsys.readouterr()

    #Defines the expected output
    expected_output = "User Profile for John Doe:\nTitle: Engineer\nMajor: Computer Science\nUniversity: Example University\nAbout: About John Doe\n"

    #Assertions
    assert captured.out == expected_output
    assert result == ("John", "Doe", "Engineer", "Computer Science", "Example University", "About John Doe")

@patch('builtins.input', side_effect=["1", "0"])
def test_view_friends_profile(mock_input, capsys):
    #Mocks the database queries
    with patch('sqlite3.connect') as mock_connect:
        mock_cursor = mock_connect.return_value.cursor.return_value

        mock_cursor.fetchall.return_value = [("friend1",), ("friend2",)]

        mock_cursor.fetchone.return_value = (("Engineer", "Computer Science", "Example University", "About friend1"),)

        #Runs the function
        view_friends_profile("user1")
        captured = capsys.readouterr()

        #Defines the expected output with normalized newline characters and removed leading whitespace
        expected_output = textwrap.dedent("""\
            Your Friends:
            1. friend1
            2. friend2
            Profile of friend1:
            Title: Engineer
            Major: Computer Science
            University: Example University
            About: About friend1
        """)

        #Normalizes captured output by removing leading/trailing whitespace and newlines
        captured_output = captured.out.strip()

        #Assertions
        assert captured_output == expected_output.strip()

if __name__ == "__main__":
    pytest.main()