import time


class DatatourismeExtractor:
	def __init__(self, api_client, checkpoint_manager, writer, page_size, page_file, time_sleep):
		self.api_client = api_client
		self.checkpoint_manager = checkpoint_manager
		self.writer = writer
		self.page_size = page_size
		self.page_file = page_file
		self.time_sleep = time_sleep

	def run(self):
		checkpoint = self.checkpoint_manager.load()

		if checkpoint:
			url = checkpoint["next_url"]
			total_count = checkpoint["total_count"]
			page_count = checkpoint["page_count"]
			file_index = checkpoint["file_index"]
		else:
			url = self.api_client.build_first_url(self.page_size)
			total_count = 0
			page_count = 0
			file_index = 1

		spinner = ["|", "/", "-", "\\"]
		spin_index = 0
		while url:
			print(f"\rProcessing {spinner[spin_index % len(spinner)]}",end="",flush=True)
			spin_index += 1

			data = self.api_client.fetch(url)
			objects = data.get("objects", [])

			self.writer.append(objects, file_index)

			page_count += 1
			total_count += len(objects)

			next_url = data.get("meta", {}).get("next")

			if page_count % 5 == 0:
				self.checkpoint_manager.save({
					"next_url": next_url,
					"total_count": total_count,
					"page_count": page_count,
					"file_index": file_index,
				})

			if page_count % self.page_file == 0:
				file_index += 1

			url = next_url
			time.sleep(self.time_sleep)

		self.checkpoint_manager.clear()
		return total_count