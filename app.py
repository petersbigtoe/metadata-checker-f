from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
import os
from PIL import Image
import piexif

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def check_metadata(file_path):
    try:
        img = Image.open(file_path)
        exif_data = img.info.get("exif")
        if not exif_data:
            return False

        exif_dict = piexif.load(exif_data)
        
        # DateTimeOriginal tag in Exif IFD is 36867
        timestamps = []
        for ifd in ("0th", "Exif"):
            for tag, value in exif_dict.get(ifd, {}).items():
                if tag == 36867:  # DateTimeOriginal
                    # piexif values are bytes, decode to str
                    ts = value.decode() if isinstance(value, bytes) else value
                    timestamps.append(ts)

        target_timestamp = "2023:01:01 00:00:00"
        count = sum(1 for ts in timestamps if ts == target_timestamp)
        return count == 3

    except Exception as e:
        print(f"Error checking metadata: {e}")
        return False

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

