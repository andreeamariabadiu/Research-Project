import hashlib
import secrets

# Mock user database
user_db = {}


def create_user(username: str, password: str, db: dict = user_db) -> bool:
    """Creates a new user and securely stores their password using PBKDF2 with a salt."""
    if username in db:
        raise ValueError("User already exists.")

    # Generate a cryptographically secure random salt (16 bytes)
    salt = secrets.token_bytes(16)
    iterations = 600_000  # OWASP recommended iterations for PBKDF2-HMAC-SHA256

    # Securely hash the password using PBKDF2
    password_hash = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=iterations,
    )

    # Store user data (salt and hash stored as hex strings; plain password is never stored)
    db[username] = {
        "salt": salt.hex(),
        "hash": password_hash.hex(),
        "iterations": iterations,
        "algorithm": "pbkdf2_sha256",
    }

    return True
