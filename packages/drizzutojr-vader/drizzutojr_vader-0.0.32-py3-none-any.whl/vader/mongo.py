import os
import json
import pymongo

from .consts import DEFAULT_MONGO_CREDS_FILE

MONGO_CREDS_FILE = os.environ.get("MONGO_CREDS_FILE", DEFAULT_MONGO_CREDS_FILE)


def get_creds() -> dict:
    mongo_creds = None
    with open(MONGO_CREDS_FILE, "r") as f:
        mongo_creds = json.load(f)

    return mongo_creds


def connect():
    mongo_creds = get_creds()

    my_client = pymongo.MongoClient(
        host=mongo_creds["address"],
        port=int(mongo_creds["port"]),
        username=mongo_creds["user"],
        password=mongo_creds["password"],
        authSource=mongo_creds["database"],
    )

    return my_client[mongo_creds["database"]]
