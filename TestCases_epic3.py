import InCollege
import pytest
import sqlite3
from unittest.mock import patch, Mock, MagicMock


@pytest.fixture
def conn():
    mock_conn = MagicMock()
    return mock_conn


def test_about_page():
    with patch('builtins.input', side_effect=['6', '2', '1']):
        with patch('builtins.print') as mock_print:
            try:
                InCollege.main()
            except Exception as e:
                pass

            lines = [
                "In College: Welcome to In College, the world's largest college student network with many users in"
                " many countries and territories worldwide. This is some information about the history and purpose"
                " of the company.",
                '1. Go back'
            ]

            for line in lines:
                mock_print.assert_any_call(line)


def test_help_center():
    with patch('builtins.input', side_effect=['5', '1', '2']):
        with patch('builtins.print') as mock_print:
            InCollege.main()

            lines = [
                "We're here to help."
            ]

            for line in lines:
                mock_print.assert_any_call(line)


def test_blog():
    with patch('builtins.input', side_effect=['5', '1', '5']):
        with patch('builtins.print') as mock_print:
            InCollege.main()

            lines = [
                "Under construction"
            ]

            for line in lines:
                mock_print.assert_any_call(line)


def test_career():
    with patch('builtins.input', side_effect=['5', '1', '6']):
        with patch('builtins.print') as mock_print:
            InCollege.main()

            lines = [
                "Under construction"
            ]

            for line in lines:
                mock_print.assert_any_call(line)


def test_business_solutions():
    with patch('builtins.input', side_effect=['5', '3']):
        with patch('builtins.print') as mock_print:
            InCollege.main()

            lines = [
                "Under construction"
            ]

            for line in lines:
                mock_print.assert_any_call(line)


def test_directories():
    with patch('builtins.input', side_effect=['5', '4']):
        with patch('builtins.print') as mock_print:
            InCollege.main()

            lines = [
                "Under construction"
            ]

            for line in lines:
                mock_print.assert_any_call(line)
