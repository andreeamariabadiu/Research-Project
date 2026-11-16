import html
import re
from typing import Any, Dict


def process_registration_form(name: Any, email: Any, age: Any) -> Dict[str, Any]:
    """Validates and sanitizes registration form input.

    Raises ValueError if any input is invalid.
    Returns a dictionary of sanitized data if successful.
    """
    errors = []

    # --- Sanitize and Validate Name ---
    if not isinstance(name, str):
        errors.append("Name must be a text string.")
        clean_name = ""
    else:
        # Strip whitespace and escape HTML entities to prevent XSS
        clean_name = html.escape(name.strip())
        if not clean_name:
            errors.append("Name cannot be empty.")
        elif not (2 <= len(clean_name) <= 50):
            errors.append("Name must be between 2 and 50 characters long.")
        elif not re.match(r"^[A-Za-z\s'-]+$", clean_name):
            errors.append(
                "Name can only contain letters, spaces, hyphens, and apostrophes."
            )

    # --- Sanitize and Validate Email ---
    if not isinstance(email, str):
        errors.append("Email must be a text string.")
        clean_email = ""
    else:
        # Normalize: strip whitespace and convert to lowercase
        clean_email = email.strip().lower()
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not clean_email:
            errors.append("Email cannot be empty.")
        elif len(clean_email) > 254:
            errors.append("Email exceeds maximum length.")
        elif not re.match(email_pattern, clean_email):
            errors.append("Invalid email address format.")

    # --- Sanitize and Validate Age ---
    clean_age = None
    try:
        if isinstance(age, (int, str)):
            clean_age = int(str(age).strip())
            if not (13 <= clean_age <= 120):
                errors.append("Age must be between 13 and 120.")
        else:
            errors.append("Age must be a number.")
    except (ValueError, TypeError):
        errors.append("Age must be a valid integer.")

    # --- Result Handling ---
    if errors:
        raise ValueError("Validation failed: " + "; ".join(errors))

    return {"name": clean_name, "email": clean_email, "age": clean_age}
