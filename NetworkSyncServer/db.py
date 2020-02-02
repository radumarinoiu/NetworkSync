import json
from pymongo import MongoClient
from bson.objectid import ObjectId

with open("logins.json", "rb") as f:
    logins = json.load(f)

client = MongoClient("mongodb://{}:{}@{}/admin".format(logins["db user"], logins["db pass"], logins["db host"]))
db = client["online-ide"]
vms_coll = db["vms"]
users_coll = db["users"]
installers_coll = db["installers"]