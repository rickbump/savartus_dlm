from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Server is running and reachable!', 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if not request.files:
        return jsonify({'error': 'No files uploaded'}), 400

    for file_key in request.files:
        file = request.files[file_key]
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        # Process each file as needed
        # file.save(os.path.join(UPLOAD_FOLDER, file.filename))

    return jsonify({'message': 'Files uploaded successfully'}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
