import re


def process_registration_form(name: str, email: str, age: int | str) -> dict:
    """Processes and validates user input from a registration form.

    Returns a dictionary indicating success status, along with either cleaned
    data or error messages.
    """
    errors = []

    # Sanitize string inputs
    cleaned_name = str(name).strip() if name is not None else ""
    cleaned_email = str(email).strip().lower() if email is not None else ""

    # Validate Name
    if not cleaned_name:
        errors.append("Name is required.")
    elif len(cleaned_name) < 2:
        errors.append("Name must be at least 2 characters long.")

    # Validate Email
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not cleaned_email:
        errors.append("Email is required.")
    elif not re.match(email_regex, cleaned_email):
        errors.append("Invalid email format.")

    # Validate Age
    parsed_age = None
    try:
        parsed_age = int(age)
        if parsed_age < 13:
            errors.append("Must be at least 13 years old to register.")
        elif parsed_age > 120:
            errors.append("Please enter a valid age.")
    except (ValueError, TypeError):
        errors.append("Age must be a valid integer.")

    if errors:
        return {"success": False, "errors": errors}

    return {
        "success": True,
        "data": {
            "name": cleaned_name.title(),
            "email": cleaned_email,
            "age": parsed_age,
        },
    }
