from mysql.connector import Error
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST, user=DB_USER,
        password=DB_PASSWORD, database=DB_NAME
    )

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("MySQL connection successful!")
        conn.close()
    except Error as e:
        print("MySQL connection failed:", e)
