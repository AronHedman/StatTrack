import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

db_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="db_pool",
    pool_size=5,
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME"),
)


def get_connection():
    return db_pool.get_connection()
