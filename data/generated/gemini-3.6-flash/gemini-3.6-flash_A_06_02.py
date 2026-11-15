from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/api/process", methods=["POST"])
def process_data():
    # Retrieve JSON data from the request body
    data = request.get_json()

    # Validate if JSON data exists
    if not data:
        return jsonify({"status": "error", "message": "No JSON data provided"}), 400

    # Process the data (example logic)
    name = data.get("name", "Anonymous")
    age = data.get("age", None)

    # Construct response
    response_data = {
        "status": "success",
        "message": f"Data received for {name}",
        "data_processed": {"name": name, "age": age},
    }

    return jsonify(response_data), 200


if __name__ == "__main__":
    app.run(debug=True)
