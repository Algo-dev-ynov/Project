from pymongo import MongoClient
from flask_api.config import Config
import ssl

class Database:
    def __init__(self):
        self.client = MongoClient(
            Config.MONGO_URI,
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        self.db = self.client[Config.MONGO_DB]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close(self):
        self.client.close()