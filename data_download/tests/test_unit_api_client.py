from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from downloader.api_client import DatatourismeApiClient


class DummyResponse:
	def __init__(self, payload, raise_error=None):
		self.payload = payload
		self.raise_error = raise_error

	def raise_for_status(self):
		if self.raise_error:
			raise self.raise_error

	def json(self):
		return self.payload


def test_build_first_url_returns_expected_url():
	client = DatatourismeApiClient(
		api_key="demo-key",
		base_url="https://example.org/api",
		timeout=12,
	)

	url = client.build_first_url(page_size=100)

	assert url == (
		"https://example.org/api?api_key=demo-key&page=1&page_size=100&lang=fr"
	)


def test_fetch_calls_requests_get_with_timeout(monkeypatch):
	client = DatatourismeApiClient(
		api_key="demo-key",
		base_url="https://example.org/api",
		timeout=42,
	)
	called = {}

	def fake_get(url, timeout):
		called["url"] = url
		called["timeout"] = timeout
		return DummyResponse({"objects": [{"id": 1}]})

	monkeypatch.setattr("requests.get", fake_get)

	payload = client.fetch("https://example.org/api?page=2")

	assert called == {
		"url": "https://example.org/api?page=2",
		"timeout": 42,
	}
	assert payload == {"objects": [{"id": 1}]}


def test_fetch_raises_when_response_status_fails(monkeypatch):
	client = DatatourismeApiClient(
		api_key="demo-key",
		base_url="https://example.org/api",
	)

	def fake_get(url, timeout):
		return DummyResponse({}, raise_error=RuntimeError("HTTP failure"))

	monkeypatch.setattr("requests.get", fake_get)

	with pytest.raises(RuntimeError, match="HTTP failure"):
		client.fetch("https://example.org/api?page=2")
