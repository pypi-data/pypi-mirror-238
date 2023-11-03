from argparse import Namespace

import sys
import os
import pytest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")

from urluckynum.app.lucky import generate_lucky_number
from urluckynum.app.lucky import show_lucky_number
from urluckynum.app.db import create_connection


@pytest.mark.unit
def test_generate_lucky_number():
    # Test the generate_lucky_number function.
    result = generate_lucky_number()

    # Assert that the result is an integer between 0 and 42 (inclusive).
    assert isinstance(result, int), "Expected an integer result"
    assert 0 <= result <= 42, "Lucky number should be between 0 and 42 (inclusive)"


@pytest.fixture
def db_connection_args(request):
    # Retrieve the command-line arguments.
    gitlab_user = request.config.getoption("--gitlab-user")
    db_name = request.config.getoption("--db-name")
    db_host = request.config.getoption("--db-host")
    db_port = request.config.getoption("--db-port")
    db_user = request.config.getoption("--db-user")
    db_password = request.config.getoption("--db-password")

    # Create a Namespace object to store the command-line arguments.
    args = Namespace(
        gitlab_user=gitlab_user,
        db_host=db_host,
        db_port=db_port,
        db_user=db_user,
        db_password=db_password,
        db_name=db_name
    )

    # Return the Namespace object as the fixture value.
    return args


@pytest.mark.integration
def test_show_lucky_number(db_connection_args):
    # Access the command-line arguments from the fixture.
    connection = create_connection(db_connection_args)

    # Assert that the connection to the database is successful.
    assert connection is not None, "Connection should not be None"

    # Try to execute the show_lucky_number function.
    try:
        show_lucky_number(connection, db_connection_args.gitlab_user)
    except Exception:
        # Assert that no exception was raised.
        assert False
    finally:
        # Close the database connection, if it is still open.
        if connection.is_connected():
            connection.close()
