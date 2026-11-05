import re
import bcrypt

from mysql.connector import IntegrityError
from database.connection import get_connection


def validate_email(email):
    pattern = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"
    return re.match(pattern, email) is not None


def register_user(name, email, password):

    name = name.strip()
    email = email.strip().lower()

    # Validate inputs
    if not name or not email or not password:
        return False, "All fields are required."

    if not validate_email(email):
        return False, "Please enter a valid email address."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Hash the password
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        query = """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
        """

        values = (name, email, hashed_password)

        cursor.execute(query, values)
        connection.commit()

        return True, "Registration successful!"

    except IntegrityError:
        if connection:
            connection.rollback()

        return False, "This email is already registered."

    except Exception:
        if connection:
            connection.rollback()

        raise

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def login_user(email, password):

    email = email.strip().lower()

    if not email or not password:
        return None

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT user_id, name, email, password
            FROM users
            WHERE email = %s
        """

        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user is None:
            return None

        stored_password = user["password"].encode("utf-8")

        # Verify password
        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password
        ):
            return {
                "user_id": user["user_id"],
                "name": user["name"],
                "email": user["email"]
            }

        return None

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()