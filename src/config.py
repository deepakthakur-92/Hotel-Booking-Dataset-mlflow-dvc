import pymongo
from dataclasses import dataclass
import os
# Provide the mongodb localhost url to connect python to mongodb.

@dataclass
class EnvironmentVariable:
    mongo_db_url = os.getenv("MONGO_DB_URL")

env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "is_canceled"