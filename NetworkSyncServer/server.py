import os

from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS

UPLOAD_FOLDER = "./tmp/"
app = Flask(__name__)
CORS(app)


@app.route('/upload_file/<upload_token>', methods=["POST"])
def upload_file(upload_token):
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
    print("Upload token: {}".format(upload_token))
    return jsonify({"token": upload_token})


@app.route('/download_file/<download_token>', methods=["GET"])
def download_file(download_token):
    print("Download token: {}".format(download_token))
    filename = "krita-4.2.8-x86_64.appimage"
    return send_file(os.path.join(UPLOAD_FOLDER, filename)), 200


if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
