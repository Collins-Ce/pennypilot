from database.connection import get_connection


def get_categories(transaction_type):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT category_id, category_name
            FROM categories
            WHERE category_type = %s
            ORDER BY category_name
        """

        cursor.execute(query, (transaction_type,))
        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def add_transaction(user_id, category_id, transaction_type,
                    amount, description, transaction_date):

    if transaction_type not in ("INCOME", "EXPENSE"):
        return False, "Invalid transaction type."

    try:
        amount = float(amount)
        if amount <= 0:
            return False, "Amount must be greater than zero."
    except (ValueError, TypeError):
        return False, "Enter a valid amount."

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO transactions
            (user_id, category_id, transaction_type,
             amount, description, transaction_date)
            SELECT %s, category_id, %s, %s, %s, %s
            FROM categories
            WHERE category_id = %s
              AND category_type = %s
        """

        cursor.execute(
            query,
            (
                user_id,
                transaction_type,
                amount,
                description.strip(),
                transaction_date,
                category_id,
                transaction_type
            )
        )

        if cursor.rowcount == 0:
            connection.rollback()
            return False, "Invalid category for this transaction type."

        connection.commit()
        return True, "Transaction added successfully."

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def get_transactions(user_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                t.transaction_id,
                t.category_id,
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
        """

        cursor.execute(query, (user_id,))
        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def update_transaction(transaction_id, user_id, category_id,
                        transaction_type, amount, description,
                        transaction_date):

    if transaction_type not in ("INCOME", "EXPENSE"):
        return False, "Invalid transaction type."

    try:
        amount = float(amount)
        if amount <= 0:
            return False, "Amount must be greater than zero."
    except (ValueError, TypeError):
        return False, "Enter a valid amount."

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE transactions
            SET category_id = %s,
                transaction_type = %s,
                amount = %s,
                description = %s,
                transaction_date = %s
            WHERE transaction_id = %s
              AND user_id = %s
              AND EXISTS (
                  SELECT 1 FROM categories
                  WHERE category_id = %s
                    AND category_type = %s
              )
        """

        cursor.execute(
            query,
            (
                category_id,
                transaction_type,
                amount,
                description.strip(),
                transaction_date,
                transaction_id,
                user_id,
                category_id,
                transaction_type
            )
        )

        connection.commit()

        if cursor.rowcount == 0:
            return False, "Transaction or category not found."

        return True, "Transaction updated successfully."

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def delete_transaction(transaction_id, user_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            DELETE FROM transactions
            WHERE transaction_id = %s
              AND user_id = %s
        """

        cursor.execute(query, (transaction_id, user_id))
        connection.commit()

        if cursor.rowcount == 0:
            return False, "Transaction not found."

        return True, "Transaction deleted successfully."

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()