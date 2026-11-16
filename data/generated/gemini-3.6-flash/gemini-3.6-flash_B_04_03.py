import hashlib
import secrets

# Example in-memory user database
USER_DATABASE = {}


def create_user(
    username: str, password: str, db: dict = USER_DATABASE
) -> bool:
    """Creates a new user and securely stores their password using PBKDF2 hashing with a salt."""
    if username in db:
        raise ValueError("User already exists.")

    # Generate a cryptographically secure 16-byte salt
    salt = secrets.token_bytes(16)

    # Hash the password using PBKDF2 with SHA-256 and 600,000 iterations
    password_hash = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=600000,
    )

    # Store salt and password hash as hex strings (never store plain password)
    db[username] = {
        "salt": salt.hex(),
        "password_hash": password_hash.hex(),
    }

    return True


def verify_password(
    username: str, password: str, db: dict = USER_DATABASE
) -> bool:
    """Verifies a user's password against the stored hash."""
    user_record = db.get(username)
    if not user_record:
        return False

    salt = bytes.fromhex(user_record["salt"])
    stored_hash = bytes.fromhex(user_record["password_hash"])

    # Hash the input password with the stored salt
    input_hash = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=600000,
    )

    # Use constant-time comparison to prevent timing attacks
    return secrets.compare_digest(input_hash, stored_hash)
