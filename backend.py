# (c) 2025 Eldiiar Bekbolotov. Licensed under the MIT License.

# Necessary imports
import psycopg2  # Python library for interacting with PostgreSQL databases.

import os  # Provides access to operating system functionalities, like environment variables.

from dotenv import (
    load_dotenv,
)  # Loads environment variables from a .env file for secure configuration.

# Load environment variables from .env
# the .env file stores sensitive data (e.g., database credentials) to keep them out of the codebase.
load_dotenv()

# Fetch variables
# Environment variables are retrieved securely using os.getenv(). These are used to configure the database connection.
USER = os.getenv("user")  # Database username.
PASSWORD = os.getenv("password")  # Database password.
HOST = os.getenv("host")  # Database server address
PORT = os.getenv("port")  # Database server port
DBNAME = os.getenv("dbname")  # Name of the database to connect to.


def connect_to_db():
    """
    Establishes a connection to the PostgreSQL database using credentials from environment variables.
    Returns:
        connection: A psycopg2 connection object if successful, None otherwise.
    """

    try:
        # Attempt to create a connection to the database using the provided credentials.
        connection = psycopg2.connect(
            user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME
        )

        print("Connection successful!")  # Log success for debugging.

        return connection
    except Exception as e:
        # Handle any connection errors (e.g., wrong credentials, network issues).
        print(f"Failed to connect: {e}")  # Log the error for debugging.

        return None


def increment_view(model_id=1):
    """
    Increments the view count for a specific model in the 'models' table.
    Args:
        model_id (int): The ID of the model to update (defaults to 1).
    """

    # Establish a database connection.
    connection = connect_to_db()

    if connection:
        # Use a context manager to ensure the cursor is properly closed.
        with connection.cursor() as cursor:
            # Execute an SQL UPDATE query to increment the 'views' column for the given model_id.
            cursor.execute(
                "UPDATE models SET views = views + 1 WHERE id = %s", (model_id,)
            )

            # Commit the transaction to save changes to the database.
            connection.commit()

        # Close the database connection to free resources.
        connection.close()


def increment_upvote(model_id=1):
    """
    Increments the upvote count for a specific model in the 'models' table.
    Args:
        model_id (int): The ID of the model to update (defaults to 1).
    """

    # Establish a database connection.
    connection = connect_to_db()

    if connection:
        # Use a context manager to ensure the cursor is properly closed.
        with connection.cursor() as cursor:
            # Execute an SQL UPDATE query to increment the 'upvotes' column for the given model_id.
            cursor.execute(
                "UPDATE models SET upvotes = upvotes + 1 WHERE id = %s", (model_id,)
            )

            # Commit the transaction to save changes to the database.
            connection.commit()
        # Close the database connection to free resources.
        connection.close()


def get_stats(model_id=1):
    """
    Retrieves the view and upvote counts for a specific model from the 'models' table.
    Args:
        model_id (int): The ID of the model to query (defaults to 1).
    Returns:
        dict: A dictionary with 'views' and 'upvotes' for the model, or zeros if no data exists.
    """

    # Establish a database connection.
    connection = connect_to_db()
    if connection:
        # Use a context manager to ensure the cursor is properly closed.
        with connection.cursor() as cursor:
            # Execute an SQL SELECT query to fetch 'views' and 'upvotes' for the given model_id.
            cursor.execute(
                "SELECT views, upvotes FROM models WHERE id = %s", (model_id,)
            )

            # Fetch the first (and only) row of the result.
            stats = cursor.fetchone()

        # Close the database connection to free resources.
        connection.close()

        if stats:
            # Return a dictionary with the retrieved stats.
            return {"views": stats[0], "upvotes": stats[1]}
        else:
            # If no data is found, return default values.
            return {"views": 0, "upvotes": 0}
