import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

# Find and load the .env file in the backend directory
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env"))
load_dotenv(dotenv_path=env_path)

db_host = os.getenv("DB_HOST", "localhost")
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "")
db_name = os.getenv("DB_NAME", "business_listings_db")
db_port = int(os.getenv("DB_PORT", "3306"))

# Configure the connection pool
db_config = {
    "host": db_host,
    "user": db_user,
    "password": db_password,
    "database": db_name,
    "port": db_port
}

try:
    db_pool = pooling.MySQLConnectionPool(
        pool_name="listings_pool",
        pool_size=5, # Pool size
        pool_reset_session=True,
        **db_config
    )
except mysql.connector.Error as err:
    print(f"Error creating connection pool: {err}")
    raise

def get_db():
    """
    FastAPI dependency that yields a database connection from the pool.
    Always releases the connection back to the pool at the end.
    """
    connection = db_pool.get_connection()
    try:
        yield connection
    finally:
        # Closes the connection (releasing it back to the pool)
        connection.close()
