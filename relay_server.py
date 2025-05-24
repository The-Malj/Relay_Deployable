from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)
UPLOAD_DIR = "upload"
PATCH_DIR = "patch"
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
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"error": "Not found"}), 404
    return send_file(path, as_attachment=True)

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
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
