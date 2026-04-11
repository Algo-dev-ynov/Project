# Bibliothèques
import requests  # Requête HTTP
import json  # Format JSON
import time  # Gère le temps
import os  # Interaction avec le système
from .downloader.api_client import DatatourismeApiClient
from .downloader.checkpoint import CheckpointManager
from .downloader.writer import NdjsonWriter
from .downloader.extractor import DatatourismeExtractor
from .downloader.picture import Picture
from dotenv import load_dotenv

load_dotenv()  # charge le .env


api_key = os.getenv("API_KEY") # Charge la clef API depuis l'env
url_api = "https://api.datatourisme.fr/v1/catalog"  # L'url de base de l'API

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Chemin
path_output = os.path.join(BASE_DIR, "..","data_lake") # Dossier de sauvegarde des données brutes au format NDJSON
path_state = os.path.join(BASE_DIR, "../data_lake", "checkpoint.json")  # Fichier qui garde la progression de l'extraction pour pouvoir reprendre en cas d'arrêt
path_picture = os.path.join(BASE_DIR, "..", "pictures")

page_file = 1000  # Nombre de pages à stocker dans un même fichier
page_size = 21  # Nombre d'objets demandés par page à l'API
time_sleep = 0.1 # Temps avant de reprendre une requête



if __name__ == "__main__":

	api_client = DatatourismeApiClient(api_key,url_api)
	checkpoint_manager = CheckpointManager(path_state)
	writer = NdjsonWriter(path_output)

	extractor = DatatourismeExtractor(api_client,checkpoint_manager,writer,page_size,page_file,time_sleep)

	total = extractor.run()
	print(f"Extraction terminée : {total} objets")


	picture = Picture(path_output,path_picture) # Objet
	# picture.process_files() # Extrait les images depuis les données et les enregistre
