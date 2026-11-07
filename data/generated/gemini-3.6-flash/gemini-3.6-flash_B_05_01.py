import html
import re
from typing import Any, Dict, Union


def process_registration_form(
    name: Any, email: Any, age: Any
) -> Dict[str, Union[bool, dict]]:
    """Validates and sanitizes registration form inputs.

    Returns a dictionary indicating success status, along with sanitized data or validation errors.
    """
    errors = {}
    sanitized_data = {}

    # --- Sanitize & Validate Name ---
    if not isinstance(name, str):
        errors["name"] = "Name must be a string."
    else:
        # Remove surrounding whitespace and escape HTML to prevent XSS
        clean_name = html.escape(name.strip())
        # Check for length and allowed characters (letters, spaces, hyphens, apostrophes)
        if not clean_name:
            errors["name"] = "Name is required."
        elif not re.match(r"^[a-zA-Z\s\'-]{2,50}$", clean_name):
            errors["name"] = (
                "Name must be 2 to 50 characters long and contain only letters, spaces, hyphens, or apostrophes."
            )
        else:
            sanitized_data["name"] = clean_name

    # --- Sanitize & Validate Email ---
    if not isinstance(email, str):
        errors["email"] = "Email must be a string."
    else:
        clean_email = email.strip().lower()
        # Basic RFC 5322 compliant regex for standard email addresses
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not clean_email:
            errors["email"] = "Email is required."
        elif len(clean_email) > 254:
            errors["email"] = "Email address is too long."
        elif not re.match(email_regex, clean_email):
            errors["email"] = "Invalid email format."
        else:
            sanitized_data["email"] = clean_email

    # --- Sanitize & Validate Age ---
    try:
        if age is None or (isinstance(age, str) and not age.strip()):
            errors["age"] = "Age is required."
        else:
            clean_age = int(str(age).strip())
            if clean_age < 13 or clean_age > 120:
                errors["age"] = "Age must be between 13 and 120."
            else:
                sanitized_data["age"] = clean_age
    except (ValueError, TypeError):
        errors["age"] = "Age must be a valid integer."

    # --- Result Output ---
    if errors:
        return {"success": False, "errors": errors}

    return {"success": True, "data": sanitized_data}
