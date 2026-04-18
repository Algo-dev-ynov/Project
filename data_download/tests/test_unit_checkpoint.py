from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from downloader.checkpoint import CheckpointManager


def test_load_returns_none_when_checkpoint_does_not_exist(tmp_path):
	manager = CheckpointManager(str(tmp_path / "checkpoint.json"))

	assert manager.load() is None


def test_save_and_load_roundtrip(tmp_path):
	checkpoint_file = tmp_path / "checkpoint.json"
	manager = CheckpointManager(str(checkpoint_file))
	state = {
		"next_url": "https://example.org/api?page=3",
		"total_count": 200,
		"page_count": 2,
		"file_index": 4,
	}

	manager.save(state)

	assert manager.load() == state


def test_clear_removes_existing_checkpoint(tmp_path):
	checkpoint_file = tmp_path / "checkpoint.json"
	manager = CheckpointManager(str(checkpoint_file))
	manager.save({"next_url": None})

	manager.clear()

	assert checkpoint_file.exists() is False
