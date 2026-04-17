import os
from dotenv import load_dotenv

"""
Module de configuration de l'application.

Charge les variables d'environnement et définit
les constantes utilisées pour la connexion à MongoDB.
"""

load_dotenv()

class Config:
    """
    Classe de configuration contenant les paramètres de base de données.

    Attributs:
        MONGO_URI (str): URI de connexion à MongoDB
        MONGO_DB (str): nom de la base de données
        COLLECTION_CLEAN (str): nom de la collection des données nettoyées
        COLLECTION_RATINGS (str): nom de la collection des avis
    """
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:root@localhost:27017/")
    MONGO_DB = os.getenv("MONGO_DB", "tourisme_data")
    COLLECTION_CLEAN = "place_clean"
    COLLECTION_RATINGS = "place_ratings"

print(f"MONGO_URI: {Config.MONGO_URI}")