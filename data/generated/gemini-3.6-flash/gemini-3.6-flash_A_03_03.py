import sqlite3


def get_user_by_name(db_path, name):
    """Retrieve user data from a SQLite database by user name.

    :param db_path: Path to the SQLite database file.
    :param name: The name of the user to query.
    :return: A list of dictionaries containing matching user records.
    """
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
