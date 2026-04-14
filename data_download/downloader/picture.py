"""
	Utility class used to extract image URLs from NDJSON files and download the images.
"""

import json
import os

import requests


class Picture:
	"""
		Handle image discovery and download from Datatourisme NDJSON output files.
	"""

	def __init__(self, path_output, path_picture):
		"""
			Initialize the picture downloader.

			Args :

				path_output: Directory containing NDJSON files.
				path_picture: Directory where images will be saved.
		"""

		self.path_output = path_output  # Folder containing NDJSON files.
		self.path_picture = path_picture  # Folder where downloaded images are stored.

	def ensure_picture_dir(self):
		"""
			Create the picture directory if it does not already exist.
		"""

		os.makedirs(self.path_picture, exist_ok=True)

	def get_locator(self, data):
		"""
			Extract the first image locator from a Datatourisme object structure.

			Args :

				data: Datatourisme object as a dictionary.

			Return :

				Image URL or None if no valid image is found.
		"""

		try:
			return data["hasMainRepresentation"][0]["hasRelatedResource"][0]["locator"][0]
		except (KeyError, IndexError, TypeError):
			# Return None when the expected nested structure is missing or incomplete.
			return None

	def get_extension_from_url(self, url):
		"""
			Detect the file extension from the image URL.

			Args :

				url: Image URL

			Return :

				File extension string.
		"""

		url = url.lower()

		# Check common image extensions directly in the URL.
		for ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
			if ext in url:
				return ext

		# Default to JPG if no known extension is detected.
		return ".jpg"

	def download_image(self, url, output_file):
		"""
			Download an image and save it to disk.

		Args :

			url: Image URL.
			output_file: Destination file path.
		"""

		response = requests.get(url, stream=True, timeout=30)
		response.raise_for_status()  # Raise an exception if the download failed.

		with open(output_file, "wb") as f:
			for chunk in response.iter_content(8192):
				if chunk:
					f.write(chunk)

	def process_files(self):
		"""
			Read all NDJSON files and download all discovered images.

			Invalid JSON lines are skipped, and already-downloaded images are not fetched again
		"""

		self.ensure_picture_dir()

		for filename in os.listdir(self.path_output):
			# Only process NDJSON files.
			if not filename.endswith(".ndjson"):
				continue

			file_path = os.path.join(self.path_output, filename)

			with open(file_path, "r", encoding="utf-8") as f:
				for line_number, line in enumerate(f, start=1):
					line = line.strip()

					# Skip empty lines.
					if not line:
						continue

					try:
						data = json.loads(line)
					except json.JSONDecodeError:
						print(f"JSON error in {filename}, line {line_number}")
						continue

					uuid = data.get("uuid")
					locator = self.get_locator(data)

					# Skip entries that do not have both an identifier and an image URL.
					if not uuid or not locator:
						continue

					extension = self.get_extension_from_url(locator)
					output_file = os.path.join(self.path_picture, f"{uuid}{extension}")

					# Avoid downloading the same image twice.
					if os.path.exists(output_file):
						continue

					try:
						self.download_image(locator, output_file)
						print(f"Downloaded: {output_file}")
					except requests.RequestException as e:
						print(f"Download error for {locator}: {e}")
