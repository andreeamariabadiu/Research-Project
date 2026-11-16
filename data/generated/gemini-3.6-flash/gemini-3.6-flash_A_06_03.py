from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'error', 'message': 'No JSON payload provided'}), 400
        
    response = {
        'status': 'success',
        'message': 'Data received successfully',
        'received_data': data
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
