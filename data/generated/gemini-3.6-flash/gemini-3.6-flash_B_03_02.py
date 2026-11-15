import sqlite3


def get_user_by_name(db_path: str, name: str):
    """Retrieves user data from a SQLite database safely using parameterized queries."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Parameterized query prevents SQL injection
        query = "SELECT * FROM users WHERE name = ?"
        cursor.execute(query, (name,))
        return cursor.fetchall()
