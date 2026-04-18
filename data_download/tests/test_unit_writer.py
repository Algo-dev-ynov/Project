from pathlib import Path
import json
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from downloader.writer import NdjsonWriter


def test_writer_creates_output_directory(tmp_path):
	output_dir = tmp_path / "output"

	writer = NdjsonWriter(str(output_dir))

	assert output_dir.exists()
	assert output_dir.is_dir()
	assert writer.output_dir == str(output_dir)


def test_get_output_filename_formats_index_with_zero_padding(tmp_path):
	writer = NdjsonWriter(str(tmp_path / "output"))

	filename = writer.get_output_filename(7)

	assert filename.endswith("data_part_0007.ndjson")


def test_append_writes_one_json_object_per_line(tmp_path):
	writer = NdjsonWriter(str(tmp_path / "output"))
	payload = [
		{"id": 1, "name": "Museum"},
		{"id": 2, "name": "Park"},
	]

	writer.append(payload, file_index=1)

	target = Path(writer.get_output_filename(1))
	lines = target.read_text(encoding="utf-8").splitlines()
	assert len(lines) == 2
	assert json.loads(lines[0]) == {"id": 1, "name": "Museum"}
	assert json.loads(lines[1]) == {"id": 2, "name": "Park"}
