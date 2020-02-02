import json


class Database(object):
    def __init__(self):
        with open("logins.json", "rb") as f:
            credentials = json.load(f)
        self.connect(credentials)
        del credentials

    def connect(self, credentials):
        pass

    def disconnect(self):
        pass

    def __del__(self):
        self.disconnect()
