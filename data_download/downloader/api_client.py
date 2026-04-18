"""
	API client for interacting with the Datatourisme API.
"""

import requests


class DatatourismeApiClient:
	"""
		Client responsible for building URLs and fetching data from the Datatourisme API.
	"""

	def __init__(self, api_key, base_url, timeout=30):
		"""
			Initialize the API client.

			Args :

				api_key: API authentication key.
				base_url: Base URL of the API.
				timeout: Request timeout in seconds.
		"""

		self.api_key = api_key
		self.base_url = base_url
		self.timeout = timeout

	def fetch(self, url):
		"""
			Send a GET request and return the parsed JSON response

			Args :

				Full URL to fetch

			Return :

				Parsed JSON response
		"""

		response = requests.get(url, timeout=self.timeout)
		response.raise_for_status()  # Raise an exception if the request failed.
		return response.json()

	def build_first_url(self, page_size):
		"""
			Build the first paginated API URL.

			Args :

				page_size: Number of items to request per page.

			Return :

				Formatted URL string.
		"""

		return f"{self.base_url}?api_key={self.api_key}&page=1&page_size={page_size}&lang=fr"
