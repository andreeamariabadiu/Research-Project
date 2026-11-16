import sqlite3
from typing import Any, List, Tuple


def get_user_by_name(db_path: str, username: str) -> List[Tuple[Any, ...]]:
    """Retrieves user data from a SQLite database by name safely using parameterized queries.

    :param db_path: Path to the SQLite database file.
    :param username: Name of the user to search for.
    :return: A list of tuples containing the matching user records.
    """
    query = "SELECT * FROM users WHERE name = ?"

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (username,))
        return cursor.fetchall()
