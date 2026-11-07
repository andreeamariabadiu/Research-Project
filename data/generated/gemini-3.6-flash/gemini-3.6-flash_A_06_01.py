from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/api/data", methods=["POST"])
def handle_post():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid or missing JSON data"}), 400

    # Process the data as needed
    response = {"status": "success", "message": "Data received", "data": data}

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True)
