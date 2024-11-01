# upload_files.py or your Flask app file

from flask import Flask, request, jsonify
from flask_cors import CORS
from db_support.process_db_support import db_connection  # Import db_connection

app = Flask(__name__)

# Update CORS configuration to match main app
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://10.0.0.5:3000"],  # Add your production domain
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

@app.route('/search_processed_files', methods=['GET'])
def search_processed_files():
    config_file = '/home/rbump/savartus_dlm/config.json'  # Path to your JSON config file
    connection = db_connection(config_file)

    if not connection:
        print("Failed to connect to database.")
        return jsonify({"error": "Could not connect to the database"}), 500

    search_query = request.args.get('query', '')
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM processed_files WHERE file_name LIKE %s", (f"%{search_query}%",))
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)