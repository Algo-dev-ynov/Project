from pymongo import MongoClient

LOCAL_URI = "mongodb://root:root@localhost:27017/"
ATLAS_URI = "mongodb+srv://karimdevweb_db_user:7U3HgeQ4Oubk3EZX@datatourisme.an0dr0v.mongodb.net/?appName=DataTourisme"

local = MongoClient(LOCAL_URI)
atlas = MongoClient(ATLAS_URI)

local_db = local["tourisme_data"]
atlas_db = atlas["tourisme_data"]

print("Récupération des 200 places...")
places = list(local_db["place_clean"].find({}).limit(200))
uuids = [p["uuid"] for p in places]

print("Récupération des ratings...")
ratings = list(local_db["place_ratings"].find({"uuid": {"$in": uuids}}))

print(f"Insertion {len(places)} places dans Atlas...")
atlas_db["place_clean"].drop()
atlas_db["place_clean"].insert_many(places)

print(f"Insertion {len(ratings)} ratings dans Atlas...")
atlas_db["place_ratings"].drop()
atlas_db["place_ratings"].insert_many(ratings)

print("Migration terminée !")
local.close()
atlas.close()