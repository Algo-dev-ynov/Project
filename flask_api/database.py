from pymongo import MongoClient
from flask_api.config import Config
import ssl

"""
Module de gestion de la connexion à la base de données MongoDB.

Ce module permet de centraliser la connexion à MongoDB
et d'accéder aux différentes collections de la base.
"""

class Database:
    """
    Classe de gestion de la connexion MongoDB.

    Permet de se connecter à la base de données et
    de récupérer les collections nécessaires.
    """

    def __init__(self):
        """
        Initialise la connexion à MongoDB.
        """
        self.client = MongoClient(
            Config.MONGO_URI,
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        self.db = self.client[Config.MONGO_DB]

    def get_collection(self, collection_name):
        """
        Récupère une collection MongoDB.

        Args:
            collection_name (str): nom de la collection

        Returns:
            Collection: collection MongoDB correspondante
        """
        return self.db[collection_name]

    def close(self):
        """
        Ferme la connexion MongoDB.
        """
        self.client.close()