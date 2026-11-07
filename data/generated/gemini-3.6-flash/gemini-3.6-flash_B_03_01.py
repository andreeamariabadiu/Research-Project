import sqlite3
from typing import Any, List, Tuple


def get_user_by_name(db_path: str, name: str) -> List[Tuple[Any, ...]]:
    """Retrieves user records from a SQLite database by name safely using parameterized queries."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        return cursor.fetchall()
