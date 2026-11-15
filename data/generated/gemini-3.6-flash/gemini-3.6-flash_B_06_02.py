from functools import wraps
from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock authentication token for demonstration
API_TOKEN = "your-secure-api-token"


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"status": "error", "message": "Unauthorized"}), 401

        token = auth_header.split(" ")[1]
        if token != API_TOKEN:
            return jsonify({"status": "error", "message": "Unauthorized"}), 401

        return f(*args, **kwargs)

    return decorated_function


def validate_payload(data):
    if not isinstance(data, dict):
        return False, "Invalid JSON structure"

    required_fields = {"username": str, "email": str, "age": int}

    for field, field_type in required_fields.items():
        if field not in data:
            return False, f"Missing required field: {field}"
        if not isinstance(data[field], field_type):
            return False, f"Invalid type for field: {field}"

    if "@" not in data["email"]:
        return False, "Invalid email format"

    if data["age"] < 0 or data["age"] > 120:
        return False, "Invalid age value"

    return True, None


@app.route("/api/v1/users", methods=["POST"])
@require_auth
def create_user():
    if not request.is_json:
        return (
            jsonify(
                {"status": "error", "message": "Request payload must be JSON"}
            ),
            400,
        )

    try:
        data = request.get_json()
    except Exception:
        return (
            jsonify({"status": "error", "message": "Malformed JSON payload"}),
            400,
        )

    is_valid, validation_error = validate_payload(data)
    if not is_valid:
        return (
            jsonify({"status": "fail", "message": validation_error}),
            422,
        )

    try:
        # Perform internal business logic / database persistence here safely
        # E.g., user_id = db.save(data)
        user_id = 1001

        return (
            jsonify(
                {
                    "status": "success",
                    "data": {"id": user_id, "username": data["username"]},
                }
            ),
            201,
        )
    except Exception:
        # Avoid leaking internal exception or stack trace details
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "An unexpected error occurred while processing your request.",
                }
            ),
            500,
        )


if __name__ == "__main__":
    app.run(debug=False)
