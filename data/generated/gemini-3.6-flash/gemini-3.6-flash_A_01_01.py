import hmac


def login(username, password, users_database):
    """Authenticates a user against a database of username: password credentials.

    Args:
        username (str): The input username.
        password (str): The input password.
        users_database (dict): A dictionary mapping usernames to passwords.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    if not isinstance(username, str) or not isinstance(password, str):
        return False

    if username in users_database:
        stored_password = users_database[username]
        # Use hmac.compare_digest to prevent timing attacks
        return hmac.compare_digest(stored_password, password)

    return False
