import logging

from threading import Lock


class StorageAgent(object):
    def __init__(self):
        self.locked_files = {}

    def download_file(self, file_id):
        pass

    def upload_file(self, file_id):
        pass
