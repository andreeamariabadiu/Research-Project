import sqlite3
from typing import Optional, Tuple


def get_user_by_name(db_path: str, name: str) -> Optional[Tuple]:
    """Fetch a user's record from a SQLite database by name.

    :param db_path: Path to the SQLite database file.
    :param name: Name of the user to search for.
    :return: A tuple containing the user's record, or None if not found.
    """
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        user_data = cursor.fetchone()
        return user_data
    finally:
        conn.close()
