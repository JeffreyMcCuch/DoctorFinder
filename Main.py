from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np
import pytesseract

app = Flask(__name__)

@app.route("/ocr", methods=["POST"])
def ocr():
    data = request.json["image"]

    # Remove header "data:image/png;base64,"
    encoded = data.split(",")[1]

    # Decode image
    img_bytes = base64.b64decode(encoded)
    npimg = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # OCR
    text = pytesseract.image_to_string(img)

    return jsonify({"text": text})

if __name__ == "__main__":
    app.run(debug=True)


