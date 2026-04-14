"""
	Datatourisme extraction module.

	This module defines the DatatourismeExtractor class, responsible for:
	- Fetching paginated data from the Datatourisme API
	- Writing results into NDJSON files
	- Managing checkpoints to allow resuming interrupted extractions
"""

import time


class DatatourismeExtractor:
	"""
		Extract paginated data from the Datatourisme API and write it into NDJSON files.

		The extractor:
		- Iterates through paginated API results
		- Writes objects to files using a writer
		- Saves progress regularly using a checkpoint system
		- Supports resuming from the last saved state
	"""

	def __init__(
		self,
		api_client,
		checkpoint_manager,
		writer,
		page_size,
		page_file,
		time_sleep,
	):
		"""
			Initialize the extractor.

			Args :

				api_client: Instance responsible for API requests.
				checkpoint_manager: Instance used to save/load progress.
				writer: Instance used to write extracted data.
				page_size: Number of objects fetched per API request.
				page_file: Number of pages stored per output file.
				time_sleep: Delay (in seconds) between API calls.
		"""

		self.api_client = api_client
		self.checkpoint_manager = checkpoint_manager
		self.writer = writer
		self.page_size = page_size
		self.page_file = page_file
		self.time_sleep = time_sleep

	def run(self):
		"""
			Execute the extraction process.

			The method:
			1. Loads a checkpoint if it exists
			2. Fetches data page by page from the API
			3. Writes results to NDJSON files
			4. Saves progress every 5 pages
			5. Splits output files based on `page_file`
			6. Clears checkpoint when finished

			Returns:

				int: Total number of objects processed.
		"""

		checkpoint = self.checkpoint_manager.load()

		# Restore previous state if a checkpoint exists
		if checkpoint:
			url = checkpoint["next_url"]
			total_count = checkpoint["total_count"]
			page_count = checkpoint["page_count"]
			file_index = checkpoint["file_index"]
		else:
			# Start from the first API page
			url = self.api_client.build_first_url(self.page_size)
			total_count = 0
			page_count = 0
			file_index = 1

		# Spinner used for simple CLI feedback
		spinner = ["|", "/", "-", "\\"]
		spin_index = 0

		while url:
			# Display progress indicator in terminal
			print(f"\rProcessing {spinner[spin_index % len(spinner)]}", end="", flush=True)
			spin_index += 1

			# Fetch data from API
			data = self.api_client.fetch(url)
			objects = data.get("objects", [])

			# Write current page objects to file
			self.writer.append(objects, file_index)

			# Update counters
			page_count += 1
			total_count += len(objects)

			# Get next page URL
			next_url = data.get("meta", {}).get("next")

			# Save checkpoint every 5 pages
			if page_count % 5 == 0:
				self.checkpoint_manager.save({
					"next_url": next_url,
					"total_count": total_count,
					"page_count": page_count,
					"file_index": file_index,
				})

			# Move to next output file after N pages
			if page_count % self.page_file == 0:
				file_index += 1

			# Prepare next iteration
			url = next_url

			# Avoid hitting API too fast
			time.sleep(self.time_sleep)

		# Cleanup checkpoint after successful completion
		self.checkpoint_manager.clear()

		return total_count