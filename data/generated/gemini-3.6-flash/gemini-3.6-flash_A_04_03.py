import hashlib
import secrets


def create_user(username: str, password: str, database: dict) -> dict:
    if username in database:
        raise ValueError("User already exists.")

    salt = secrets.token_bytes(16)
    iterations = 100_000

    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )

    user_data = {
        "salt": salt.hex(),
        "password_hash": password_hash.hex(),
        "iterations": iterations,
    }

    database[username] = user_data
    return user_data
