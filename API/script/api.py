# Bibliothèques
import requests # Requête html
import json # Format JSON
import time # Gère le temps
import os # Interraction avec le système

API_KEY = "a28db3a7-7c19-4721-b1c7-bb5c76250566"  # Variable globale qui sera la clef d'authentification de l'API
BASE_URL = "https://api.datatourisme.fr/v1/catalog" # L'url de base de l'API

OUTPUT_FILE = "data_raw.json" # Fichier de sauvegarde des données
STATE_FILE = "checkpoint.json" # Fichier qui garde la progression de l'extraction pour pouvoir reprendre en cas d'arrêt

def fetch_with_retry(url, retries=8, timeout=30):
	"""
	Fait une requête GET avec gestion des erreurs et retry sur 429 / erreurs temporaires.

	@param url : Url à appeler
	@param retries : Nombre maximal de tentatives
	@param timeout : Délai maximal d'attente d'une réponse HTP avant erreur
	"""

	for attempt in range(retries): # Boucle de répétition
		try:
			response = requests.get(url, timeout=timeout) # Requête pour récupérer les données avec un timeout entre chaque requête

			if response.status_code == 200: # Gère les erreurs des requêtes
				return response.json() # Renvoie les données

			if response.status_code == 429: # Gère l'erreur "trop de requête"
				wait_time = min(2 ** attempt, 60) # Calcule le temps d'attente
				print(f"[429] Trop de requêtes. Nouvelle tentative dans {wait_time}s...")
				time.sleep(wait_time) # Le programme attend
				continue # Interruption de la boucle

			if 500 <= response.status_code < 600: # Gère les erreurs serveur
				wait_time = min(2 ** attempt, 60) # Calculel e temps d'attente
				print(f"[{response.status_code}] Erreur serveur. Nouvelle tentative dans {wait_time}s...")
				time.sleep(wait_time) # Le programme attend
				continue # Interruption de la boucle

			print(f"Erreur HTTP {response.status_code}") # Gère les autres erreurs
			print(response.text)
			return None # Pas de résultat

		except requests.exceptions.RequestException as e: # Intercepte les exceptions
			wait_time = min(2 ** attempt, 60) #Calcule le temps d'attente
			print(f"Erreur réseau : {e}")
			print(f"Nouvelle tentative dans {wait_time}s...")
			time.sleep(wait_time) # Le programme attend

	print("Échec après plusieurs tentatives.")
	return None # Pas de résultat


def save_json(data, filename=OUTPUT_FILE):
	'''
		Sauvegarde des données dans un fichier JSON

		@param data : Données à enregistrer
		@param filename : Nom du fichier où sauvegarder les donénes
	'''

	with open(filename, "w", encoding="utf-8") as f: # Ouvre le fichier en mode écriture
		json.dump(data, f, ensure_ascii=False, indent=2)  # Écrit les données Python dans le fichier au format JSON
	print(f"Fichier sauvegardé : {filename}")


def save_checkpoint(next_url, total_count, page_count, state_file=STATE_FILE):
	'''
		Sauvegarde l'état de l'extraction

		@param next_url : Prochaine URL à appeler
		@param total_count : Nombre totla d'objets récupérés
		@param page_count : Nombre de pages déjà traités
		@param stage_file : Nom du fichier checkpoint
	'''

	checkpoint = { # Dictionnaire python
		"next_url": next_url,
		"total_count": total_count,
		"page_count": page_count,
	}
	with open(state_file, "w", encoding="utf-8") as f: # Ouvre le fichier checkpoint
		json.dump(checkpoint, f, ensure_ascii=False, indent=2) # Sauvegarde le dictionnaire dnas le fichier JSON


def load_checkpoint(state_file=STATE_FILE):
	''''
		Lit le fichier checkpoint

		@param state_file : Fichier checkpoint
	'''

	if not os.path.exists(state_file): # Vérifie si le fichier existe
		return None # Pas de résultat

	with open(state_file, "r", encoding="utf-8") as f: # Ouvre le fichier de checkpoint en lecture
		return json.load(f) # Renvoie les données sous le format dictionnaire Pyhon


def load_existing_data(filename=OUTPUT_FILE):
	'''
		Relaire les données déjà sauvegardées

		@param filename : Nom du fichier
	'''

	if not os.path.exists(filename): # Vérifie si le fichier existe
		return [] # Renvoie une liste vide si n'existe pas

	with open(filename, "r", encoding="utf-8") as f: # Ouvre le fichier en lecture
		return json.load(f) # Charge le contenu du fichier


def extract_data():
	'''
		Extrait les données
	'''

	checkpoint = load_checkpoint() # Appelle la fonction pour voir s'il existe un état de reprise

	if checkpoint: # Vérifie si cehckpoint est vide ou non
		print("Checkpoint trouvé. Reprise en cours...")
		url = checkpoint["next_url"] # Récupère l'URL stockée dans le chckpoint
		page_count = checkpoint["page_count"] # Récupère le nombre de pages déjà traités
		all_objects = load_existing_data() # Recharge le fichier de données pour récupérer les objets déjà extraits
		print(f"Reprise depuis page ~{page_count + 1} | Objets déjà sauvegardés : {len(all_objects)}")
	else: # Démarre une extraction neuve
		url = f"{BASE_URL}?api_key={API_KEY}&page=1&page_size=250&lang=fr" # Construit l'URL
		page_count = 0  # Initialise le compteur de pages à 9
		all_objects = [] # Initialise une liste qui contiendra tous les objets récupérés

	while url: # Tant que url n'est pas None ou vide
		print(f"Requête : {url}")

		data = fetch_with_retry(url) # Appelle la fonction de requête robuste
		if not data: # Vérifie si data est vide
			print("Arrêt de l'extraction à cause d'une erreur.")
			save_json(all_objects, OUTPUT_FILE) # Sauvegarde les données 
			save_checkpoint(url, len(all_objects), page_count) # Sauvegarde le checkpoint
			return all_objects # Retourne la liste de données

		objects = data.get("objects", []) # Récupère la valeur associée à la clef du dictionnaire data
		all_objects.extend(objects) # Ajoute tous les éléments à la liste

		page_count += 1 # Incrément" le compteur de page
		print(f"Page {page_count} récupérée | Total : {len(all_objects)} objets")

		next_url = data.get("meta", {}).get("next") # Cherche l'URL de la page suivante

		if page_count % 5 == 0: # Vérifie si la page est un multiple de 5
			print("Sauvegarde intermédiaire...")
			save_json(all_objects, OUTPUT_FILE) # Sauvegarde tous les objets accumulées jusqu'ici
			save_checkpoint(next_url, len(all_objects), page_count) # Sauvegarde aussi le point de reprise

		url = next_url # Met à jour l'url suivante
		time.sleep(4.0) # Le programme attend

	save_json(all_objects, OUTPUT_FILE) # Quand la boucle se termine, sauvegarde finale

	if os.path.exists(STATE_FILE): # Vérifie si le fichier temporaire existe
		os.remove(STATE_FILE) # Supprime le fichier temporaire
		print("Checkpoint supprimé : extraction terminée.")

	return all_objects # Retourne la liste complète des objets


if __name__ == "__main__": # Vérifie si le fichier est exécuté directement
	print("Début extraction...")

	data = extract_data() # Appelle la fonction qui extrait les données

	print(f"Extraction terminée : {len(data)} objets")
