import time
import logging

from pymongo import MongoClient
from bson.objectid import ObjectId
from NetworkSyncServer.db import Database


class MongoDatabase(Database):
    def __init__(self):
        super(MongoDatabase, self).__init__()

    # noinspection PyAttributeOutsideInit
    def connect(self, credentials):
        self._client = MongoClient(
            "mongodb://{}:{}@{}/admin".format(
                credentials["db user"],
                credentials["db pass"],
                credentials["db host"]))
        self._db = self._client["netsync"]
        self._archived_files = self._db["archived-files"]
        self._garbage_collection = self._db["garbage-collection"]
        self._file_tokens = self._db["file-tokens"]
        self._stored_files = self._db["stored-files"]

    def disconnect(self):
        self._client.close()

    def generate_upload_token(self, file_path, file_sha256_checksum):
        return self._file_tokens.insert_one({
            "timestamp": time.time(),
            "file path": file_path,
            "sha256sum": file_sha256_checksum
        }).inserted_id

    def use_upload_token_and_get_path(self, upload_token):
        file_token_data = self._file_tokens.find_one_and_delete({"_id": ObjectId(upload_token)})
        return file_token_data

    def register_file(self, file_path, file_token):
        self._stored_files.insert_one({
            "timestamp": time.time(),
            "file path": file_path,
            "_id": ObjectId(file_token)})
