from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/detect-darts', methods=['POST'])
def detect_darts():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    # Mocking a response for testing
    mock_detections = [
        {'x1': 50, 'y1': 50, 'x2': 100, 'y2': 100, 'confidence': 0.95, 'class': 'dart'},
        {'x1': 150, 'y1': 150, 'x2': 200, 'y2': 200, 'confidence': 0.90, 'class': 'dart'}
    ]
    
    return jsonify(mock_detections)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
