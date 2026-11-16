import re


def process_registration_form(name: str, email: str, age: str | int) -> dict:
    """Processes, sanitizes, and validates registration form inputs."""
    errors = []

    # Sanitize and validate Name
    clean_name = str(name).strip() if name else ""
    if not clean_name:
        errors.append("Name is required.")
    elif len(clean_name) < 2:
        errors.append("Name must be at least 2 characters long.")

    # Sanitize and validate Email
    clean_email = str(email).strip().lower() if email else ""
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not clean_email:
        errors.append("Email is required.")
    elif not re.match(email_regex, clean_email):
        errors.append("Invalid email format.")

    # Validate and convert Age
    parsed_age = None
    try:
        parsed_age = int(age)
        if parsed_age < 13 or parsed_age > 120:
            errors.append("Age must be between 13 and 120.")
    except (ValueError, TypeError):
        errors.append("Age must be a valid integer.")

    if errors:
        return {"success": False, "errors": errors, "data": None}

    return {
        "success": True,
        "errors": [],
        "data": {
            "name": clean_name.title(),
            "email": clean_email,
            "age": parsed_age,
        },
    }
