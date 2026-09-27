from flask import Flask
from flask_cors import CORS
import mysql.connector

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

app = Flask(__name__)
CORS(app)


# MySQL connection
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


@app.route("/")
def home():
    return {
        "message": "Survival Hub Backend is running!"
    }


if __name__ == "__main__":
    app.run(debug=True)