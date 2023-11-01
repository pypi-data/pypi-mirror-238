import mysql.connector

# Function that executes a query on the MySQL db and returns the fetched results.
def execute_query(connection, query, values=None):
    """Executes a query on the MySQL db and returns the fetched results.

    Args:
        connection: A MySQL connection object.
        query: The SQL query to be executed.
        values: A list of values to be bound to the query parameters, or None if
            there are no parameters.

    Returns:
        A list of rows returned by the query, or None if the query failed.
    """

    try:
        cursor = connection.cursor()

        if values is not None:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        results = cursor.fetchall()

        cursor.close()
        connection.commit()  # Avoid lack of commit.

        return results
    except mysql.connector.Error as err:
        print(f"Query execution error: {err}")
        return None