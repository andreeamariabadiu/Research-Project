import hashlib
import os

# Simulated database
USER_DATABASE = {}


def create_user(username: str, password: str, db: dict = USER_DATABASE) -> bool:
    """Securely creates a new user and stores the salted and hashed password."""
    if username in db:
        raise ValueError("Username already exists.")

    # Generate a random 32-byte salt
    salt = os.urandom(32)

    # Hash the password using PBKDF2 with SHA-256
    password_hash = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=100000,
    )

    # Store salt and password hash as hex strings
    db[username] = {
        "salt": salt.hex(),
        "password_hash": password_hash.hex(),
    }

    return True
