from flask import Flask, request, send_file, render_template
import subprocess
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Use 'exiftool' from PATH; if not found, raise error on startup
EXIFTOOL_PATH = shutil.which("exiftool")
if EXIFTOOL_PATH is None:
    raise RuntimeError("Exiftool not found in PATH. Please install exiftool in your environment.")

def check_metadata(file_path):
    try:
        # Run exiftool to get metadata
        result = subprocess.run(
            [EXIFTOOL_PATH, file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True  # returns output as string, no need to decode
        )
    except subprocess.CalledProcessError as e:
        # Handle exiftool failure (e.g., corrupted file)
        print("Exiftool error:", e.stderr)
        return False

    target_timestamp = "2023:01:01 00:00:00"
    count = sum(1 for line in result.stdout.splitlines() if target_timestamp in line)
    return count == 3

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    if check_metadata(file_path):
        return send_file("flag.txt", as_attachment=True)
    else:
        return "❌ Metadata not set correctly. Exactly 3 timestamps must be 2023:01:01 00:00:00", 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
