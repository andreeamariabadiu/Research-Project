import hmac


def login(username, password, user_database):
    """Authenticates a user against a database dictionary.

    Parameters:
    - username (str): The username supplied by the user.
    - password (str): The password supplied by the user.
    - user_database (dict): A dictionary mapping usernames to correct passwords.

    Returns:
    - bool: True if credentials are valid, False otherwise.
    """
    if username not in user_database:
        return False

    stored_password = user_database[username]

    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(stored_password, password)
