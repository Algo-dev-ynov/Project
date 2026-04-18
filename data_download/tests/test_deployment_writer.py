from pathlib import Path
import json
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from downloader.writer import NdjsonWriter


def test_writer_smoke_appends_multiple_batches_to_same_file(tmp_path):
	writer = NdjsonWriter(str(tmp_path / "output"))

	writer.append([{"id": 1}, {"id": 2}], file_index=1)
	writer.append([{"id": 3}], file_index=1)

	target = Path(writer.get_output_filename(1))
	lines = target.read_text(encoding="utf-8").splitlines()

	assert [json.loads(line) for line in lines] == [
		{"id": 1},
		{"id": 2},
		{"id": 3},
	]
