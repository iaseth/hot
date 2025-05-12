import datetime



class Snapshot:
	def __init__(self, time_machine):
		self.time_machine = time_machine
		self.hotdoc = self.time_machine.hotdoc
		self.hash = self.hotdoc.hash
		self.json_text = self.hotdoc.json_text

		self.datetime = datetime.datetime.now()
		self.dts = str(self.datetime)[:19]
		self.date = self.dts[:10]
		self.time = self.dts[11:]

	def __repr__(self):
		return f"Snapshot ({self.hash}) on {self.date} at {self.time}"


