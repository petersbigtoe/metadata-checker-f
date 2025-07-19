from flask import Flask, request, send_file, render_template_string
import subprocess
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def check_metadata(file_path):
    result = subprocess.run(['exiftool', file_path], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    target_timestamp = "2023:01:01 00:00:00"
    count = sum(1 for line in output.splitlines() if target_timestamp in line)
    return count == 3

@app.route('/')
def index():
    with open('index.html') as f:
        return render_template_string(f.read())

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
        return "❌ Metadata not set correctly. Hint: 3 timestamps must be EXACTLY 2023:01:01 00:00:00", 400

if __name__ == '__main__':
    app.run(debug=True)
