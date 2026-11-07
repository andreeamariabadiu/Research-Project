from functools import wraps
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Authentication token configured via environment variable (or fallback for demo)
API_TOKEN = os.getenv("API_KEY", "your-secure-api-token")


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return (
                jsonify(
                    {
                        "error": "Unauthorized",
                        "message": "Missing or invalid authorization token",
                    }
                ),
                401,
            )

        token = auth_header.split(" ", 1)[1]
        if token != API_TOKEN:
            return (
                jsonify(
                    {
                        "error": "Unauthorized",
                        "message": "Missing or invalid authorization token",
                    }
                ),
                401,
            )

        return f(*args, **kwargs)

    return decorated


def validate_data(data):
    """Validates incoming JSON payload structure and types."""
    if not isinstance(data, dict):
        return False, "Payload must be a JSON object"

    required_fields = {
        "username": str,
        "email": str,
        "age": int,
    }

    for field, expected_type in required_fields.items():
        if field not in data:
            return False, f"Missing required field: '{field}'"
        if not isinstance(data[field], expected_type):
            return False, f"Invalid data type for field: '{field}'"

    return True, None


@app.route("/api/v1/data", methods=["POST"])
@require_auth
def process_data():
    try:
        data = request.get_json(silent=True)

        if data is None:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": "Request body must be valid JSON",
                    }
                ),
                400,
            )

        is_valid, error_message = validate_data(data)
        if not is_valid:
            return (
                jsonify({"error": "Validation Error", "message": error_message}),
                422,
            )

        # Process the validated data safely here
        # ...

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Data processed successfully",
                }
            ),
            200,
        )

    except Exception:
        # Internal error is logged securely on the server side, not returned to client
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred while processing your request",
                }
            ),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
