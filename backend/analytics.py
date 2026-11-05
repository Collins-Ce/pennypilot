from database.connection import get_connection


def get_dashboard_data(user_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Calculate income and expenses for this user.
        summary_query = """
            SELECT
                COALESCE(SUM(
                    CASE WHEN transaction_type = 'INCOME'
                    THEN amount ELSE 0 END
                ), 0) AS total_income,

                COALESCE(SUM(
                    CASE WHEN transaction_type = 'EXPENSE'
                    THEN amount ELSE 0 END
                ), 0) AS total_expenses

            FROM transactions
            WHERE user_id = %s
        """

        cursor.execute(summary_query, (user_id,))
        summary = cursor.fetchone()

        total_income = summary["total_income"]
        total_expenses = summary["total_expenses"]
        balance = total_income - total_expenses

        # Fetch the five most recent transactions.
        recent_query = """
            SELECT
                t.transaction_id,
                t.transaction_type,
                t.amount,
                t.description,
                t.transaction_date,
                c.category_name

            FROM transactions t

            JOIN categories c
                ON t.category_id = c.category_id

            WHERE t.user_id = %s

            ORDER BY t.transaction_date DESC,
                     t.transaction_id DESC

            LIMIT 5
        """

        cursor.execute(recent_query, (user_id,))
        recent_transactions = cursor.fetchall()

        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance,
            "recent_transactions": recent_transactions
        }

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()