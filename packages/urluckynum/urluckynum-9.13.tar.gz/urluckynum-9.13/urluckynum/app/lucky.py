import secrets
from urluckynum.app.queries import execute_query


def generate_lucky_number():
    """Generates a random integer in [0, 42].

    Returns:
        A random integer in [0, 42].
    """

    return secrets.randbelow(43)


def show_lucky_number(connection, gitlab_user):
    """Shows the lucky number for the given GitLab user.

    Args:
        connection: A MySQL connection object.
        gitlab_user: The GitLab username.

    Preconditions:
        The GitLab username must be valid and have a maximum length of 255 characters.
        The MySQL connection must be valid.

    Postconditions:
        The lucky number for the given GitLab user is printed to the console.

    Raises:
        RuntimeError: If the `create_table_sql` query fails, or if the `check_user_sql` query fails,
            or if the `insert_user_sql` query fails (for new users).
    """

    # Create the `users` table if it doesn't already exist.
    create_table_sql = (
        "CREATE TABLE IF NOT EXISTS `sys`.`users` ("
        "`gitlab_user` VARCHAR(255) NOT NULL,"
        "`lucky_number` INT NOT NULL,"
        "PRIMARY KEY (`gitlab_user`),"
        "UNIQUE INDEX `gitlab_user_UNIQUE` (`gitlab_user` ASC) VISIBLE);"
    )
    if execute_query(connection, create_table_sql) is None:
        raise RuntimeError("Failed to create table users")

    # Check if the user already exists.
    check_user_sql = "SELECT COUNT(*) FROM `users` WHERE `gitlab_user` = %s"
    result = execute_query(connection, check_user_sql, (gitlab_user,))
    if result is None:
        raise RuntimeError("Failed to check if user has already requested the service before")

    # Extract the value.
    result = result[0][0]

    # Is the user new?
    new_user = result == 0

    # Generate a lucky number for new users.
    if new_user:
        lucky_number = generate_lucky_number()

        # Insert the user's lucky number into the database.
        insert_user_sql = "INSERT INTO `users` VALUES (%s, %s)"
        values = (gitlab_user, lucky_number)
        if execute_query(connection, insert_user_sql, values) is None:
            raise RuntimeError("Failed to insert the lucky number in the db for new user")

    # Retrieve the user's lucky number, for both old and new users.
    select_lucky_number_sql = "SELECT `lucky_number` FROM `users` WHERE `gitlab_user` = %s"
    result = execute_query(connection, select_lucky_number_sql, (gitlab_user,))[0][0]

    # Generate the output message.
    welcome_message = "Hi" if new_user else "Welcome back"

    # Print the output message to the console.
    print(f"{welcome_message} {gitlab_user}! Your lucky number is {result}")