from unittest.mock import patch, MagicMock
import pytest
from InCollege import send_message


@pytest.fixture
def mock_cursor():
    with patch('sqlite3.connect') as mock_connect:
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        yield mock_cursor


@pytest.fixture
def mock_input():
    with patch('builtins.input') as mock:
        mock.side_effect = ['1', 'Test message']
        yield mock


@pytest.fixture
def mock_print():
    with patch('builtins.print') as mock:
        yield mock


LOGGED_IN_USER = 'standard_user'


@patch('InCollege.LOGGED_IN_USER', LOGGED_IN_USER)
def test_send_message_standard_user(mock_cursor, mock_input, mock_print):
    mock_cursor.fetchall.return_value = [('friend1',), ('friend2',)]
    send_message(LOGGED_IN_USER)
    mock_print.assert_called()
    mock_cursor.execute.assert_called()
    assert mock_input.call_count == 2


@patch('InCollege.LOGGED_IN_USER', 'plus_user')
def test_send_message_plus_user(mock_cursor, mock_input, mock_print):
    mock_cursor.fetchall.return_value = [('friend1',), ('friend2',)]
    send_message('plus_user')
    mock_print.assert_called()
    mock_cursor.execute.assert_called()
    assert mock_input.call_count == 2
