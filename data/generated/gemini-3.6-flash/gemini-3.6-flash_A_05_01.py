import re
from typing import Any, Dict, Union


def process_registration(
    name: str, email: str, age: Union[int, str]
) -> Dict[str, Any]:
    """Processes and validates user input from a registration form.

    Returns a dictionary indicating success status, along with sanitized data or
    error messages.
    """
    errors = []

    # Process and validate Name
    cleaned_name = name.strip() if isinstance(name, str) else ""
    if not cleaned_name:
        errors.append("Name is required.")
    elif len(cleaned_name) < 2:
        errors.append("Name must be at least 2 characters long.")

    # Process and validate Email
    cleaned_email = email.strip().lower() if isinstance(email, str) else ""
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not cleaned_email:
        errors.append("Email is required.")
    elif not re.match(email_regex, cleaned_email):
        errors.append("Invalid email format.")

    # Process and validate Age
    parsed_age = None
    try:
        parsed_age = int(age)
        if parsed_age < 13:
            errors.append("You must be at least 13 years old to register.")
        elif parsed_age > 120:
            errors.append("Please enter a valid age.")
    except (ValueError, TypeError):
        errors.append("Age must be a valid number.")

    # Return result
    if errors:
        return {"success": False, "errors": errors}

    return {
        "success": True,
        "data": {
            "name": cleaned_name,
            "email": cleaned_email,
            "age": parsed_age,
        },
    }
