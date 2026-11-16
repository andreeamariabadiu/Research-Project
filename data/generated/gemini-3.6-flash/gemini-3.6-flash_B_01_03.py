import re
import bcrypt
import sqlite3
from typing import Optional


def sanitize_input(input_string: str, max_length: int = 255) -> Optional[str]:
    """Sanitizes string input by stripping whitespace and checking constraints."""
    if not isinstance(input_string, str):
        return None
    cleaned = input_string.strip()
    if not cleaned or len(cleaned) > max_length:
        return None
    return cleaned


def authenticate_user(
    db_connection: sqlite3.Connection, username: str, password: str
) -> bool:
    """Authenticates a user securely against SQL injection and timing attacks."""
    # 1. Input Sanitization and Validation
    clean_username = sanitize_input(username, max_length=50)
    clean_password = sanitize_input(password, max_length=128)

    # Basic format validation (alphanumeric, underscores, hyphens, @, .)
    if not clean_username or not clean_password:
        return False
    if not re.match(r"^[a-zA-Z0-9_.\-@]+$", clean_username):
        return False

    # Pre-calculated dummy hash to mitigate timing attacks when user is not found
    dummy_hash = b"$2b$12$e868d45869d67e6c1e550u9tW/n2N7A.J67DqD8JvR8E67e6c1e55"

    try:
        cursor = db_connection.cursor()

        # 2. SQL Injection Protection (Parameterized Query)
        query = "SELECT password_hash FROM users WHERE username = ?"
        cursor.execute(query, (clean_username,))
        result = cursor.fetchone()

        if result:
            stored_hash = result[0]
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode("utf-8")
        else:
            # Perform dummy comparison to keep response time consistent
            stored_hash = dummy_hash

        # 3. Secure Password Verification
        password_bytes = clean_password.encode("utf-8")
        is_valid = bcrypt.checkpw(password_bytes, stored_hash)

        return is_valid if result else False

    except sqlite3.Error:
        return False
