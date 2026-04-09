import json
import os


class CheckpointManager:
	def __init__(self, path_state):
		self.path_state = path_state

	def save(self, state):
		with open(self.path_state, "w", encoding="utf-8") as f:
			json.dump(state, f, ensure_ascii=False, indent=2)

	def load(self):
		if not os.path.exists(self.path_state):
			return None

		with open(self.path_state, "r", encoding="utf-8") as f:
			return json.load(f)

	def clear(self):
		if os.path.exists(self.path_state):
			os.remove(self.path_state)