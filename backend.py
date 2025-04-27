# (c) 2025 Eldiiar Bekbolotov. Licensed under the MIT License.

# Necessary imports
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Connect to the database using the pooler
def connect_to_db():
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        print("Connection successful!")
        return connection
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

# Increment view counter for a specific model
def increment_view(model_id=1):
    connection = connect_to_db()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE models SET views = views + 1 WHERE id = %s", (model_id,))
            connection.commit()
        connection.close()

# Increment upvote counter for a specific model
def increment_upvote(model_id=1):
    connection = connect_to_db()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE models SET upvotes = upvotes + 1 WHERE id = %s", (model_id,))
            connection.commit()
        connection.close()

# Get the current stats for a specific model
def get_stats(model_id=1):
    connection = connect_to_db()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT views, upvotes FROM models WHERE id = %s", (model_id,))
            stats = cursor.fetchone()
        connection.close()
        if stats:
            return {"views": stats[0], "upvotes": stats[1]}
        else:
            return {"views": 0, "upvotes": 0}
