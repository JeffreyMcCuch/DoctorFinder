from flask import Flask, request, jsonify, send_file
import base64
import cv2
import numpy as np
import pytesseract
import shutil
import os

app = Flask(__name__, static_folder='.', static_url_path='')


def ensure_tesseract():
    """Ensure tesseract executable is available. Return True if found, False otherwise."""
    # If it's on PATH, shutil.which will find it
    if shutil.which("tesseract"):
        return True

    # Common installation paths on Windows
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    for p in possible_paths:
        if os.path.exists(p):
            pytesseract.pytesseract.tesseract_cmd = p
            return True

    return False


@app.route("/")
def serve_index():
    return send_file("Main.html", mimetype="text/html")


@app.route("/ocr", methods=["POST"])
def ocr():
    if not request.is_json:
        return jsonify({"error": "Invalid request, expected JSON"}), 400

    data = request.json.get("image")
    if not data:
        return jsonify({"error": "No image provided"}), 400

    if not ensure_tesseract():
        return jsonify({
            "error": "Tesseract not found",
            "details": "Install Tesseract-OCR and ensure it's on PATH or set pytesseract.pytesseract.tesseract_cmd to its installation path."
        }), 500

    try:
        # Remove header "data:image/png;base64,"
        encoded = data.split(",")[1]

        # Decode image
        img_bytes = base64.b64decode(encoded)
        npimg = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # OCR
        text = pytesseract.image_to_string(img)

        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": "OCR failed", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)


