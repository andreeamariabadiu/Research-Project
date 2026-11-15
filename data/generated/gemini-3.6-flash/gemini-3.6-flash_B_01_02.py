import hashlib
import hmac
import re
import sqlite3
from typing import Optional, Tuple


def sanitize_input(input_str: str) -> str:
    """Sanitize string input by stripping whitespace and removing control characters."""
    if not isinstance(input_str, str):
        return ""
    # Strip whitespace and remove unprintable control characters
    cleaned = input_str.strip()
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", cleaned)
    return cleaned


def hash_password(
    password: str, salt: Optional[bytes] = None
) -> Tuple[bytes, bytes]:
    """Securely hash a password using PBKDF2 with SHA-256."""
    if salt is None:
        import os

        salt = os.urandom(32)  # Generate a random 32-byte salt

    iterations = 600000  # OWASP recommended iteration count for PBKDF2-HMAC-SHA256
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )
    return password_hash, salt


def verify_password(
    provided_password: str, stored_hash: bytes, stored_salt: bytes
) -> bool:
    """Verify a provided password against the stored hash and salt in constant time."""
    computed_hash, _ = hash_password(provided_password, stored_salt)
    return hmac.compare_digest(stored_hash, computed_hash)


def login_user(db_connection: sqlite3.Connection, username: str, password: str) -> bool:
    """Authenticate a user safely against SQL injection and password attacks."""
    # 1. Input Sanitization and Validation
    username = sanitize_input(username)
    if not username or not password or not isinstance(password, str):
        return False

    # Enforce basic constraints (e.g., length limits)
    if len(username) > 64 or len(password) > 128:
        return False

    # 2. Parameterized SQL Query (Protects against SQL Injection)
    cursor = db_connection.cursor()
    query = "SELECT password_hash, salt FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    record = cursor.fetchone()

    # 3. Secure Verification
    if record is None:
        # Mitigate timing attacks by performing a dummy hash comparison
        dummy_salt = b"\x00" * 32
        dummy_hash = b"\x00" * 32
        verify_password(password, dummy_hash, dummy_salt)
        return False

    stored_hash, stored_salt = record

    # Check password using constant-time comparison
    return verify_password(password, stored_hash, stored_salt)
