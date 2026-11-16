import hashlib


def login(username, password, user_db):
    """Authenticates a user against a database storing hashed passwords.

    :param username: str - Username provided by the user.
    :param password: str - Plaintext password provided by the user.
    :param user_db: dict - Database mapping usernames to SHA-256 hashed
    passwords.
    :return: tuple - (bool success, str message)
    """
    if not username or not password:
        return False, "Username and password are required."

    if username not in user_db:
        return False, "Invalid username or password."

    # Hash the input password using SHA-256
    hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

    # Compare hashed input password with stored hash
    if user_db[username] == hashed_password:
        return True, "Login successful."

    return False, "Invalid username or password."


# Example Usage:
if __name__ == "__main__":
    # Mock database storing SHA-256 hashed passwords
    # "secure123" -> 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918
    mock_db = {
        "admin": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
    }

    # Successful login attempt
    success, message = login("admin", "secure123", mock_db)
    print(f"Success: {success}, Message: {message}")

    # Failed login attempt
    success, message = login("admin", "wrongpassword", mock_db)
    print(f"Success: {success}, Message: {message}")
