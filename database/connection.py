import os
from pathlib import Path

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


# Locate the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")


def get_connection():

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", "3306"))
        )

        if connection.is_connected():
            return connection

    except (Error, ValueError) as e:
        raise RuntimeError(
            f"Database connection failed: {e}"
        ) from e

    raise RuntimeError("Could not establish database connection.")