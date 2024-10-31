
# my_flask_app.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS(app)  # This will enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for
app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Adjust origins as needed
@app.route('/')
def home():
    return 'Server is running and reachable!', 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Here you can save the file or just respond with success for testing
    # file.save(os.path.join(UPLOAD_FOLDER, file.filename))

    return jsonify({'message': 'File uploaded successfully'}), 200

@app.route('/search_processed_files', methods=['GET'])
def search_processed_files():
    query = request.args.get('query')
    response_data = [{
        "id": 1,
        "file_name": "file1.txt",
        "file_size": "2MB",
        "file_type": "text",
        "process_date": "2023-08-01",
        "additional_data": "Example data"
    }]
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
