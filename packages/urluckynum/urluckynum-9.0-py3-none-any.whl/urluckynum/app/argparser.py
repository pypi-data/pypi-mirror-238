import argparse

def create_parser():
    """Creates an argument parser for the application.

    The parser supports the following arguments:
        --gitlab-user: The GitLab username.
        --db-name: The database name. (default: sys)
        --db-host: The database host address.
        --db-port: The database port number.
        --db-user: The database username.
        --db-password: The database password.

    Returns:
        An argument parser object.
    """

    parser = argparse.ArgumentParser(description="App with database connection")

    parser.add_argument("--gitlab-user", type=str, help="GitLab user name")
    parser.add_argument("--db-name", type=str, help="Database name", default="sys")
    parser.add_argument("--db-host", type=str, help="Database host address")
    parser.add_argument("--db-port", type=int, help="Database port number")
    parser.add_argument("--db-user", type=str, help="Database username")
    parser.add_argument("--db-password", type=str, help="Database password")

    return parser
