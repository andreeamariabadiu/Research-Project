import hashlib
import hmac
import re
import sqlite3
from typing import Optional


def sanitize_input(input_string: str, max_length: int = 256) -> Optional[str]:
    """Validates and sanitizes string input."""
    if not isinstance(input_string, str):
        return None
    cleaned = input_string.strip()
    if not cleaned or len(cleaned) > max_length:
        return None
    return cleaned


def authenticate_user(
    username: str, password: str, db_connection: sqlite3.Connection
) -> bool:
    """Authenticates a user securely against SQL injection and timing attacks."""
    # 1. Input Sanitization & Validation
    sanitized_username = sanitize_input(username, max_length=50)
    if not sanitized_username or not isinstance(password, str) or not password:
        return False

    # Ensure username contains only safe characters (alphanumeric, dots, underscores, hyphens)
    if not re.match(r"^[a-zA-Z0-9._-]+$", sanitized_username):
        return False

    # Dummy salt and hash used to mitigate timing attacks if user is not found
    dummy_salt = b"static_dummy_salt_for_timing_protection"
    dummy_hash = hashlib.scrypt(
        b"dummy_password", salt=dummy_salt, n=16384, r=8, p=1
    )

    # 2. Parameterized SQL Query (Prevents SQL Injection)
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT password_hash, salt FROM users WHERE username = ?",
        (sanitized_username,),
    )
    row = cursor.fetchone()

    if row:
        stored_hash, stored_salt = row
    else:
        # Perform fake calculation to keep execution time constant
        stored_hash, stored_salt = dummy_hash, dummy_salt

    # 3. Secure Hash Verification using scrypt and Constant-Time Comparison
    try:
        computed_hash = hashlib.scrypt(
            password.encode("utf-8"), salt=stored_salt, n=16384, r=8, p=1
        )
        # hmac.compare_digest prevents timing side-channel attacks
        is_valid = hmac.compare_digest(computed_hash, stored_hash)
    except Exception:
        is_valid = False

    return is_valid if row else False
