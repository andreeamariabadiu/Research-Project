import functools
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Authentication token configuration
API_TOKEN = os.getenv("API_TOKEN", "default-secret-token")


def require_auth(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401

        token = auth_header.split(" ", 1)[1]
        if token != API_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401

        return f(*args, **kwargs)

    return decorated


def validate_payload(data):
    """Validates incoming JSON schema without raising detailed system errors."""
    if not isinstance(data, dict):
        return False, "Invalid payload format"

    required_fields = {"username": str, "email": str, "age": int}

    for field, field_type in required_fields.items():
        if field not in data:
            return False, "Missing required fields"
        if not isinstance(data[field], field_type):
            return False, "Invalid data types provided"

    if "@" not in data["email"] or len(data["email"]) < 5:
        return False, "Invalid email address format"

    if data["age"] < 0 or data["age"] > 120:
        return False, "Invalid age value"

    return True, None


@app.route("/api/v1/users", methods=["POST"])
@require_auth
def create_user():
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 415

        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Malformed JSON payload"}), 400

        is_valid, error_message = validate_payload(data)
        if not is_valid:
            return jsonify({"error": error_message}), 400

        # Simulate internal business logic/database operation safely
        user_id = 1001  # Placeholder for created resource ID

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Resource processed successfully",
                    "id": user_id,
                }
            ),
            201,
        )

    except Exception:
        # Catch internal errors to prevent exposing stack traces or backend implementation details
        return jsonify({"error": "An internal error occurred"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
