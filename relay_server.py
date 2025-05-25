from flask import Flask, request, jsonify
from werkzeug.utils import safe_join
import os
import json

app = Flask(__name__)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "upload")
PATCH_DIR = os.path.join(os.path.dirname(__file__), "patch")
AUTH_TOKEN = "spherex-secret-token"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PATCH_DIR, exist_ok=True)

def authorized(req):
    return req.headers.get("Authorization") == f"Bearer {AUTH_TOKEN}"

@app.route("/upload", methods=["POST"])
def upload():
    if not authorized(request):
        return jsonify({"error": "Unauthorized"}), 403
    f = request.files.get("file")
    if not f:
        return jsonify({"error": "No file uploaded"}), 400
    f.save(os.path.join(UPLOAD_DIR, f.filename))
    return jsonify({"message": "Upload successful", "filename": f.filename})

@app.route("/latest", methods=["GET"])
def latest():
    files = os.listdir(UPLOAD_DIR)
    return jsonify({"files": files})

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    filepath = safe_join(UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "Not found"}), 404
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/patch", methods=["POST"])
def upload_patch():
    if not authorized(request):
        return jsonify({"error": "Unauthorized"}), 403
    f = request.files.get("file")
    if not f:
        return jsonify({"error": "No file uploaded"}), 400
    f.save(os.path.join(PATCH_DIR, f.filename))
    return jsonify({"message": "Patch uploaded", "filename": f.filename})

@app.route("/patch.zip", methods=["GET"])
def download_patch():
    path = os.path.join(PATCH_DIR, "gpt_patch.zip")
    if not os.path.exists(path):
        return jsonify({"error": "No patch available"}), 404
    with open(path, "rb") as f:
        content = f.read()
    return app.response_class(content, mimetype="application/zip")

@app.route("/status")
def status():
    files = os.listdir(UPLOAD_DIR)
    return jsonify({"auto_mode": False, "files": files})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
