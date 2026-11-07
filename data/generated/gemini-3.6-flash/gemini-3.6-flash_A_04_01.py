import hashlib
import secrets
import sqlite3


def create_user(username, password, db_path="users.db"):
    """Hashes the user's password securely and stores the new user in a SQLite database."""
    salt = secrets.token_bytes(16)
    iterations = 600000

    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )

    stored_value = f"{iterations}:{salt.hex()}:{password_hash.hex()}"

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        )

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, stored_value),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
