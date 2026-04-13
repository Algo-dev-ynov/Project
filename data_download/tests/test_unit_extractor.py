from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from downloader.extractor import DatatourismeExtractor


class FakeApiClient:
	def __init__(self, responses=None):
		self.responses = responses or []
		self.build_calls = []
		self.fetch_calls = []

	def build_first_url(self, page_size):
		self.build_calls.append(page_size)
		return "https://example.org/api?page=1"

	def fetch(self, url):
		self.fetch_calls.append(url)
		return self.responses.pop(0)


class FakeCheckpointManager:
	def __init__(self, checkpoint=None):
		self.checkpoint = checkpoint
		self.saved_states = []
		self.cleared = False

	def load(self):
		return self.checkpoint

	def save(self, state):
		self.saved_states.append(state)

	def clear(self):
		self.cleared = True


class FakeWriter:
	def __init__(self):
		self.calls = []

	def append(self, data, file_index):
		self.calls.append((data, file_index))


def test_run_starts_from_first_url_when_no_checkpoint(monkeypatch):
	api_client = FakeApiClient(
		responses=[
			{
				"objects": [{"id": 1}, {"id": 2}],
				"meta": {"next": None},
			}
		]
	)
	checkpoint_manager = FakeCheckpointManager(checkpoint=None)
	writer = FakeWriter()
	extractor = DatatourismeExtractor(
		api_client=api_client,
		checkpoint_manager=checkpoint_manager,
		writer=writer,
		page_size=2,
		page_file=10,
		time_sleep=0,
	)

	monkeypatch.setattr("time.sleep", lambda *_: None)

	total = extractor.run()

	assert api_client.build_calls == [2]
	assert api_client.fetch_calls == ["https://example.org/api?page=1"]
	assert writer.calls == [([{"id": 1}, {"id": 2}], 1)]
	assert total == 2
	assert checkpoint_manager.cleared is True


def test_run_resumes_from_checkpoint(monkeypatch):
	api_client = FakeApiClient(
		responses=[
			{
				"objects": [{"id": 5}],
				"meta": {"next": None},
			}
		]
	)
	checkpoint_manager = FakeCheckpointManager(
		checkpoint={
			"next_url": "https://example.org/api?page=3",
			"total_count": 4,
			"page_count": 2,
			"file_index": 2,
		}
	)
	writer = FakeWriter()
	extractor = DatatourismeExtractor(
		api_client=api_client,
		checkpoint_manager=checkpoint_manager,
		writer=writer,
		page_size=2,
		page_file=10,
		time_sleep=0,
	)

	monkeypatch.setattr("time.sleep", lambda *_: None)

	total = extractor.run()

	assert api_client.build_calls == []
	assert api_client.fetch_calls == ["https://example.org/api?page=3"]
	assert writer.calls == [([{"id": 5}], 2)]
	assert total == 5


def test_run_saves_checkpoint_every_five_pages(monkeypatch):
	responses = []
	for page_number in range(1, 6):
		responses.append(
			{
				"objects": [{"id": page_number}],
				"meta": {
					"next": None
					if page_number == 5
					else f"https://example.org/api?page={page_number + 1}"
				},
			}
		)

	api_client = FakeApiClient(responses=responses)
	checkpoint_manager = FakeCheckpointManager(checkpoint=None)
	writer = FakeWriter()
	extractor = DatatourismeExtractor(
		api_client=api_client,
		checkpoint_manager=checkpoint_manager,
		writer=writer,
		page_size=1,
		page_file=10,
		time_sleep=0,
	)

	monkeypatch.setattr("time.sleep", lambda *_: None)

	total = extractor.run()

	assert total == 5
	assert checkpoint_manager.saved_states == [
		{
			"next_url": None,
			"total_count": 5,
			"page_count": 5,
			"file_index": 1,
		}
	]


def test_run_increments_output_file_index_based_on_page_file(monkeypatch):
	api_client = FakeApiClient(
		responses=[
			{
				"objects": [{"id": 1}],
				"meta": {"next": "https://example.org/api?page=2"},
			},
			{
				"objects": [{"id": 2}],
				"meta": {"next": "https://example.org/api?page=3"},
			},
			{
				"objects": [{"id": 3}],
				"meta": {"next": None},
			},
		]
	)
	checkpoint_manager = FakeCheckpointManager(checkpoint=None)
	writer = FakeWriter()
	extractor = DatatourismeExtractor(
		api_client=api_client,
		checkpoint_manager=checkpoint_manager,
		writer=writer,
		page_size=1,
		page_file=2,
		time_sleep=0,
	)

	monkeypatch.setattr("time.sleep", lambda *_: None)

	extractor.run()

	assert writer.calls == [
		([{"id": 1}], 1),
		([{"id": 2}], 1),
		([{"id": 3}], 2),
	]
