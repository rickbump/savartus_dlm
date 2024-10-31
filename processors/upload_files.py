
from flask import Flask, request, jsonify
import os
os.environ["FLASK_ENV"] = "production"
import subprocess
from flask_cors import CORS

app = Flask(__name__)
#CORS(app, resources={r"/upload": {"origins": "*"}})  # Allow all origins or specify the frontend's origin URL for security
CORS(app, resources={r"/*": {"origins": ["http://10.0.0.5:3000"]}})  # Set this to your frontend's IP and port

# CORS(app, resources={r"/upload": {"origins": "http://yourfrontenddomain.com"}})

UPLOAD_FOLDER = '/home/rbump/savartus_dlm/uploads'  # Change this to the directory on your Azure box
# MAX_FILE_SIZE = 15 * 1024 * 1024  # 5 MB file size limit

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_files = []
    # Ensure the uploads directory exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if 'file0' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    # Loop through files in the form data
    for key in request.files:
        file = request.files[key]
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        # Save the file to a directory (adjust this to your needs)
        save_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(save_path)
        uploaded_files.append(save_path)  # Store the saved file path

        # Call main_ingest.py with the list of uploaded files
        try:
            result = subprocess.run(
                ["python3", "/home/rbump/savartus_dlm/main_ingest.py"] + uploaded_files,
                check=True, capture_output=True, text=True
            )
            # Return the standard output of main_ingest.py
            return jsonify({'status': 'success', 'message': 'Files successfully uploaded and processed',
                            'output': result.stdout}), 200
#        try:
#           subprocess.run(["python3", "/home/rbump/savartus_dlm/main_ingest.py"] + uploaded_files, check=True)
        except subprocess.CalledProcessError as e:
            return jsonify({'error': 'Error running main_ingest.py'}), 500

        return jsonify({'status': 'success', 'message': 'Files successfully uploaded and processed'}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)  # Explicitly disable debug