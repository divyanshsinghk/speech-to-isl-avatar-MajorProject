from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

from main import run_pipeline

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "temp_audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    if "audio" not in request.files:
        return jsonify({"error": "No audio provided"}), 400

    file = request.files["audio"]

    filepath = os.path.join(UPLOAD_FOLDER, "input.webm")
    file.save(filepath)

    try:
        result = run_pipeline(filepath)

        # Safety defaults
        result.setdefault("text", "")
        result.setdefault("tokens", [])
        result.setdefault("videos", {})

        return jsonify(result)

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)