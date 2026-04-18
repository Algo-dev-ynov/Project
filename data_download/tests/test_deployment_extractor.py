from pathlib import Path
import json
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from downloader.api_client import DatatourismeApiClient
from downloader.checkpoint import CheckpointManager
from downloader.extractor import DatatourismeExtractor
from downloader.writer import NdjsonWriter


def test_extractor_smoke_runs_end_to_end_without_checkpoint(monkeypatch, tmp_path):
	api_client = DatatourismeApiClient(
		api_key="demo-key",
		base_url="https://example.org/api",
		timeout=5,
	)
	checkpoint_manager = CheckpointManager(str(tmp_path / "checkpoint.json"))
	writer = NdjsonWriter(str(tmp_path / "output"))
	responses = [
		{
			"objects": [{"id": 1}, {"id": 2}],
			"meta": {"next": "https://example.org/api?page=2"},
		},
		{
			"objects": [{"id": 3}],
			"meta": {"next": None},
		},
	]

	def fake_fetch(url):
		return responses.pop(0)

	monkeypatch.setattr(api_client, "fetch", fake_fetch)
	monkeypatch.setattr("time.sleep", lambda *_: None)

	extractor = DatatourismeExtractor(
		api_client=api_client,
		checkpoint_manager=checkpoint_manager,
		writer=writer,
		page_size=2,
		page_file=10,
		time_sleep=0,
	)

	total = extractor.run()

	output_file = Path(writer.get_output_filename(1))
	lines = output_file.read_text(encoding="utf-8").splitlines()

	assert total == 3
	assert [json.loads(line) for line in lines] == [
		{"id": 1},
		{"id": 2},
		{"id": 3},
	]
	assert not Path(checkpoint_manager.path_state).exists()


def test_extractor_smoke_resumes_from_real_checkpoint(monkeypatch, tmp_path):
	api_client = DatatourismeApiClient(
		api_key="demo-key",
		base_url="https://example.org/api",
		timeout=5,
	)
	checkpoint_manager = CheckpointManager(str(tmp_path / "checkpoint.json"))
	writer = NdjsonWriter(str(tmp_path / "output"))
	checkpoint_manager.save(
		{
			"next_url": "https://example.org/api?page=3",
			"total_count": 4,
			"page_count": 2,
			"file_index": 2,
		}
	)
	seen_urls = []

	def fake_fetch(url):
		seen_urls.append(url)
		return {
			"objects": [{"id": 5}, {"id": 6}],
			"meta": {"next": None},
		}

	monkeypatch.setattr(api_client, "fetch", fake_fetch)
	monkeypatch.setattr("time.sleep", lambda *_: None)

	extractor = DatatourismeExtractor(
		api_client=api_client,
		checkpoint_manager=checkpoint_manager,
		writer=writer,
		page_size=2,
		page_file=10,
		time_sleep=0,
	)

	total = extractor.run()

	output_file = Path(writer.get_output_filename(2))
	lines = output_file.read_text(encoding="utf-8").splitlines()

	assert seen_urls == ["https://example.org/api?page=3"]
	assert total == 6
	assert [json.loads(line) for line in lines] == [
		{"id": 5},
		{"id": 6},
	]
	assert not Path(checkpoint_manager.path_state).exists()
