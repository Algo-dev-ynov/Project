"""
	Checkpoint manager used to save and restore extraction state.
"""

import json
import os


class CheckpointManager:
	"""
		Handle checkpoint persistence so the extraction can resume after interruption.
	"""

	def __init__(self, path_state):
		"""
			Initialize the checkpoint manager.

			Args :

				path_state: Path to the checkpoint file.
		"""

		self.path_state = path_state

	def save(self, state):
		"""
			Save the current state to disk as JSON.

			Args :

				state: Dictionary containing the checkpoint data.
		"""

		with open(self.path_state, "w", encoding="utf-8") as f:
			json.dump(state, f, ensure_ascii=False, indent=2)

	def load(self):
		"""
			Load the checkpoint from disk if it exists.

			Args :

			Checkpoint dictionary or None if no checkpoint file exists.
		"""

		if not os.path.exists(self.path_state):
			return None

		with open(self.path_state, "r", encoding="utf-8") as f:
			return json.load(f)

	def clear(self):
		"""
			Delete the checkpoint file if it exists.
		"""

		if os.path.exists(self.path_state):
			os.remove(self.path_state)
