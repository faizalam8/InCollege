# Test Cases for Epic 6
import InCollege
import pytest
import sqlite3
import io
from unittest.mock import patch, Mock, MagicMock
from InCollege import post_job, num_jobs, view_all_jobs, view_saved_jobs, login, save_job

@pytest.fixture
def mock_db():
    with patch('InCollege.sqlite3.connect') as mock_conn:
        mock_conn.cursor.return_value = MagicMock()
        yield mock_conn

# function to provide limited inputs
def limited_input(inputs):
    for input in inputs:
        yield input
    raise RuntimeError("Too many input calls")

@pytest.fixture
def mock_input(inputs):
    with patch('InCollege.input', side_effect=limited_input(inputs)):
        yield

@pytest.fixture
def mock_job_search():
    with patch('InCollege.job_search'):
        yield

@pytest.mark.parametrize("existing_jobs, expected_output, inputs", [
    (10, '10 jobs have already been posted', ['1']),
    (9, 'Success! Your job has been posted', ['Job Title', 'Description', 'Employer', 'Location', '50000'])
])
# test that at most 10 jobs can be posted
def test_post_job(mock_db, mock_input, mock_job_search, existing_jobs, expected_output, inputs, capsys):
    with patch('InCollege.input', side_effect=limited_input(inputs)):
        with patch('InCollege.num_jobs', return_value=existing_jobs):
            post_job()
            captured = capsys.readouterr()
            assert expected_output in captured.out

# check the list posted jobs
@pytest.fixture
def mock_db():
    with patch("sqlite3.connect") as mock_connect:
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ('Job1', 'Description1', 'Employer1', 'Location1', 'Salary1'),
            ('Job2', 'Description2', 'Employer2', 'Location2', 'Salary2'),
        ]
        mock_connect.return_value.cursor.return_value = mock_cursor
        yield

@pytest.fixture
def mock_num_jobs():
    with patch('InCollege.num_jobs', return_value=2):
        yield

@pytest.fixture
def mock_input():
    inputs = ['1','0', '3', '8', '10']
    with patch('builtins.input', side_effect=inputs):
        yield

def test_view_all_jobs(mock_db, mock_num_jobs, mock_input, capsys):
    InCollege.view_all_jobs()

    captured = capsys.readouterr()
    output = captured.out

    assert "Job1" in output
    assert "Description1" in output
    assert "Employer1" in output
    assert "Job2" in output
    assert "Description2" in output
    assert "Employer2" in output

# check list for saved jobs
def test_display_saved_jobs(monkeypatch):
    printed_lines = []
    monkeypatch.setattr('builtins.print', lambda *args: printed_lines.append(' '.join(map(str, args))))
    monkeypatch.setattr('builtins.input', lambda _: '1')

    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [('Job Title 1',), ('Job Title 2',)]
    with patch('InCollege.sqlite3.connect') as mock_connect:
        mock_connect.return_value.cursor.return_value = mock_cursor

        InCollege.view_saved_jobs()

    expected_output = [
        'You have saved the following jobs:',
        '1. Job Title 1',
        '2. Job Title 2',
        '3. Go back', 
        'Selecting a job will unsave it',
        'Job removed from saved list!'  
    ]
    assert printed_lines == expected_output

# check lists are there after login
def test_job_persistence(mocker):

    with patch('builtins.input') as mock_input, patch('InCollege.view_all_jobs') as mock_get_posted_jobs:
        mock_input.side_effect = ['2']
        InCollege.job_search()

        mock_get_posted_jobs.assert_called_once()

def test_saved_job_persistance():
    with patch('builtins.input') as mock_input, patch('InCollege.view_saved_jobs') as mock_get_saved_jobs:
        mock_input.side_effect = ['5']
        InCollege.job_search()

        mock_get_saved_jobs.assert_called_once()
