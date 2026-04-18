"""
	Writer utility for storing extracted objects in NDJSON format.
"""

import json
import os


class NdjsonWriter:
	"""
		Write extracted objects into chunked NDJSON files.
	"""

	def __init__(self, output_dir):
		"""
			Initialize the writer and ensure the output directory exists.

			Args :

				output_dir: Directory where NDJSON files will be written.
		"""

		self.output_dir = output_dir
		os.makedirs(self.output_dir, exist_ok=True)

	def get_output_filename(self, file_index):
		"""
			Build the output filename for a given file index

			Args :

				file_index: Numeric file index

			Return :

				Full path of the NDJSON output file
		"""

		return os.path.join(self.output_dir, f"data_part_{file_index:04d}.ndjson")

	def append(self, data, file_index):
		"""
			Append a list of objects to the target NDJSON file

			Args :

				data: Iterable of JSON-serializable objects
				file_index: Target output file index
		"""

		filename = self.get_output_filename(file_index)
		with open(filename, "a", encoding="utf-8") as f:
			for item in data:
				# Write one JSON object per line to follow the NDJSON format.
				f.write(json.dumps(item, ensure_ascii=False) + "\n")
