import json
import os


class NdjsonWriter:
	def __init__(self, output_dir):
		self.output_dir = output_dir
		os.makedirs(self.output_dir, exist_ok=True)

	def get_output_filename(self, file_index):
		return os.path.join(self.output_dir, f"data_part_{file_index:04d}.ndjson")

	def append(self, data, file_index):
		filename = self.get_output_filename(file_index)
		with open(filename, "a", encoding="utf-8") as f:
			for item in data:
				f.write(json.dumps(item, ensure_ascii=False) + "\n")