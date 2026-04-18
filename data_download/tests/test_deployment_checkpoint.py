from pathlib import Path
import json
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from downloader.checkpoint import CheckpointManager


def test_checkpoint_smoke_save_load_and_clear(tmp_path):
	checkpoint_file = tmp_path / "checkpoint.json"
	manager = CheckpointManager(str(checkpoint_file))
	state = {
		"next_url": "https://example.org/api?page=6",
		"total_count": 123,
		"page_count": 5,
		"file_index": 2,
	}

	manager.save(state)

	assert checkpoint_file.exists()
	assert json.loads(checkpoint_file.read_text(encoding="utf-8")) == state
	assert manager.load() == state

	manager.clear()

	assert not checkpoint_file.exists()
