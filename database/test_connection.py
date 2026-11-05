from database.connection import get_connection


def test_database():

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        print("================================")
        print("      PENNYPILOT DATABASE")
        print("================================")

        cursor.execute("SELECT DATABASE()")
        database = cursor.fetchone()

        print("Connected to:", database[0])

        cursor.execute("SHOW TABLES")

        print("\nAvailable Tables:")

        for table in cursor.fetchall():
            print("-", table[0])

        cursor.execute("SELECT COUNT(*) FROM categories")
        count = cursor.fetchone()[0]

        print("\nTotal Categories:", count)

        print("\nDatabase connection successful!")

    except Exception as e:
        print("Error:", e)

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    test_database()