from flask import Flask, request, jsonify, render_template
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import pandas as pd
import joblib
from utils import extract_features
from threat_api import check_with_google_safe_browsing

app = Flask(__name__)
model = joblib.load("model.pkl")

GOOGLE_API_KEY = "AIzaSyB8CHRdgn2NglwlOaWQhdBShz9XDbN_Is4"  # 🔐 Replace with your actual key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze_qr", methods=["POST"])
def analyze_qr():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]

    try:
        # Decode QR image
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        decoded = decode(img)
        if not decoded:
            return jsonify({"error": "No QR code found"})

        # Extract URL
        url = decoded[0].data.decode('utf-8')

        # Feature extraction
        features = extract_features(url)
        input_df = pd.DataFrame([features])

        # ML model prediction
        score = model.predict_proba(input_df)[0][1]
        result = "malicious" if score > 0.5 else "benign"

        # Google Safe Browsing check
        google_flag = check_with_google_safe_browsing(GOOGLE_API_KEY, url)
        if google_flag:
            result = "malicious (Google Verified)"
            score = 1.0  # override for total risk

        # Trust score and risk level
        trust_score = round((1 - score) * 100, 2)
        if trust_score >= 80:
            risk_level = "Low"
        elif trust_score >= 40:
            risk_level = "Medium"
        else:
            risk_level = "High"

        # Final response
        return jsonify({
            "url": url,
            "trust_score": trust_score,
            "risk_level": risk_level,
            "result": result
        })

    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
