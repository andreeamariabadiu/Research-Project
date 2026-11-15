import html
import re
from typing import Any, Dict


def process_registration_input(
    raw_name: Any, raw_email: Any, raw_age: Any
) -> Dict[str, Any]:
    errors = {}
    sanitized_data = {}

    # --- 1. Validate & Sanitize Name ---
    if not isinstance(raw_name, str):
        errors["name"] = "Name must be a string."
    else:
        # Sanitize: strip whitespace and escape HTML entities to prevent XSS
        clean_name = html.escape(raw_name.strip())
        if not clean_name:
            errors["name"] = "Name cannot be empty."
        elif len(clean_name) < 2 or len(clean_name) > 50:
            errors["name"] = "Name must be between 2 and 50 characters."
        elif not re.match(r"^[A-Za-z\s\'-]+$", clean_name):
            errors["name"] = (
                "Name can only contain letters, spaces, hyphens, and apostrophes."
            )
        else:
            sanitized_data["name"] = clean_name.title()

    # --- 2. Validate & Sanitize Email ---
    if not isinstance(raw_email, str):
        errors["email"] = "Email must be a string."
    else:
        # Sanitize: strip whitespace and convert to lowercase
        clean_email = raw_email.strip().lower()
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not clean_email:
            errors["email"] = "Email is required."
        elif len(clean_email) > 254:
            errors["email"] = "Email is too long."
        elif not re.match(email_regex, clean_email):
            errors["email"] = "Invalid email address format."
        else:
            sanitized_data["email"] = clean_email

    # --- 3. Validate & Sanitize Age ---
    try:
        if isinstance(raw_age, str):
            raw_age = raw_age.strip()
        age = int(raw_age)

        if age < 13 or age > 120:
            errors["age"] = "Age must be between 13 and 120."
        else:
            sanitized_data["age"] = age
    except (ValueError, TypeError):
        errors["age"] = "Age must be a valid whole number."

    # Return result dictionary
    if errors:
        return {"success": False, "errors": errors, "data": None}

    return {"success": True, "errors": None, "data": sanitized_data}
