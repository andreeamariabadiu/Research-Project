import hashlib
import secrets

# Simulated database storage
USER_DATABASE = {}


def create_user(username: str, password: str) -> dict:
    """Creates a new user record with a securely hashed password using PBKDF2 and a random salt."""
    if username in USER_DATABASE:
        raise ValueError("User already exists.")

    # Generate a secure random salt (16 bytes)
    salt = secrets.token_bytes(16)

    # Hash the password using PBKDF2-HMAC-SHA256 with 600,000 iterations
    iterations = 600_000
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )

    # Store salt and hash, never the plaintext password
    user_record = {
        "username": username,
        "salt": salt,
        "password_hash": password_hash,
        "iterations": iterations,
    }

    USER_DATABASE[username] = user_record
    return {"status": "success", "username": username}
