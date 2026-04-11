import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:root@localhost:27017/")
    MONGO_DB = os.getenv("MONGO_DB", "tourisme_data")
    COLLECTION_CLEAN = "place_clean"
    COLLECTION_RATINGS = "place_ratings"

print(f"MONGO_URI: {Config.MONGO_URI}")
    