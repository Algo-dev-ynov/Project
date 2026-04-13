from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from downloader.api_client import DatatourismeApiClient


class DummyResponse:
	def raise_for_status(self):
		return None

	def json(self):
		return {
			"objects": [{"id": 1}, {"id": 2}],
			"meta": {"next": None},
		}


def test_api_client_smoke_builds_first_url_and_fetches_payload(monkeypatch):
	client = DatatourismeApiClient(
		api_key="demo-key",
		base_url="https://example.org/api",
		timeout=5,
	)
	requested_urls = []

	def fake_get(url, timeout):
		requested_urls.append((url, timeout))
		return DummyResponse()

	monkeypatch.setattr("requests.get", fake_get)

	first_url = client.build_first_url(page_size=2)
	payload = client.fetch(first_url)

	assert requested_urls == [(first_url, 5)]
	assert payload["objects"] == [{"id": 1}, {"id": 2}]
	assert payload["meta"]["next"] is None
