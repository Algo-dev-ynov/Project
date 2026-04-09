import requests


class DatatourismeApiClient:
	def __init__(self, api_key, base_url, timeout=30):
		self.api_key = api_key
		self.base_url = base_url
		self.timeout = timeout

	def fetch(self, url):
		response = requests.get(url, timeout=self.timeout)
		response.raise_for_status()
		return response.json()

	def build_first_url(self, page_size):
		return f"{self.base_url}?api_key={self.api_key}&page=1&page_size={page_size}&lang=fr"