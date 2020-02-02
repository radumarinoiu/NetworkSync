import os
import logging

from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS

from NetworkSyncServer.mongodb import MongoDatabase
from NetworkSyncServer.utils import file_sha256sum

UPLOAD_FOLDER = "./tmp/"
app = Flask(__name__)
CORS(app)

db = MongoDatabase()


@app.route('/file_changed_event', methods=["POST", "DELETE"])
def file_changed_event():
    if request.method == "POST":
        request_json = request.get_json()
        if "path" in request_json and "sha256sum" in request_json:
            file_path = request_json["path"]
            file_sha256_checksum = request_json["sha256sum"]
            upload_token = db.generate_upload_token(file_path, file_sha256_checksum)
            return jsonify({"upload token": str(upload_token)}), 201
        logging.error("Path/Sha256sum missing for generating upload token from {}".format(request.remote_addr))
        return jsonify({"error": "Path/Sha256sum missing!"}), 400
    elif request.method == "DELETE":
        pass


@app.route('/upload_file/<upload_token>', methods=["POST"])
def upload_file(upload_token):
    file_data = db.use_upload_token_and_get_path(upload_token=upload_token)

    if file_data:
        if request.stream:
            file_path = os.path.join(UPLOAD_FOLDER, upload_token)

            with open(file_path, "wb") as fd:
                while not request.stream.is_exhausted:
                    fd.write(request.stream.read(65536))

            file_hash = file_sha256sum(file_path)

            if file_data["sha256sum"] == file_hash:
                db.register_file(file_path=file_data["file path"], file_token=upload_token)
                return jsonify({"token": upload_token}), 201

            logging.error("Data integrity check failed for upload token {} from {}".format(
                upload_token, request.remote_addr))
            return jsonify({"error": "No data was sent!"}), 400

        logging.error("No data stream sent for upload token {} from {}".format(upload_token, request.remote_addr))
        return jsonify({"error": "No data was sent!"}), 400
    else:
        logging.error("Invalid upload token {} from {}".format(upload_token, request.remote_addr))
        return jsonify({"error": "Invalid upload token!"}), 404


@app.route('/download_file/', methods=["GET"])
def download_file():

    return send_file(os.path.join(UPLOAD_FOLDER, filename)), 200


if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
