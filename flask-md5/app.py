# import libraries
from flask import Flask, request, render_template_string
import hashlib
import os

# Initialize the Flask application
app = Flask(__name__)

# Define the folder where uploaded files will be stored temporarily
UPLOAD_FOLDER = '/uploads'

# Create the upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HTML template for the web interface
HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>MD5 Hash Generator</title>
</head>
<body>
    <h1>Select a file to MD5 hash</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Upload</button>
    </form>
    {% if filename %}
    <h2>File: {{ filename }}</h2>
    {% endif %}
    {% if hash %}
    <h2>MD5 Hash: {{ hash }}</h2>
    {% endif %}
</body>
</html>
'''

# Route for the main page, render the html template
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Route for handling file uploads, when the upload button is pushed or request is sent to /upload as the URI
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the file part is in the request
    if 'file' not in request.files:
        return "No file part", 400
    
    # Get the file from the request
    file = request.files['file']
    
    # Check if the filename is empty
    if file.filename == '':
        return "No selected file", 400

    # Save the file to the upload folder
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Calculate MD5 hash
    md5_hash = calculate_md5(file_path)

    # Delete the file after hashing
    os.remove(file_path)
    
    # Render the template with the filename and MD5 hash
    return render_template_string(HTML_TEMPLATE, hash=md5_hash, filename=file.filename)

# Function to calculate MD5 hash of a file
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    
# Run the Flask application with debugging off
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
