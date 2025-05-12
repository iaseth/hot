import datetime



class Snapshot:
	def __init__(self, doc):
		self.hash = doc.hash
		self.json_text = doc.json_text
		self.datetime = datetime.datetime.now()
		self.dts = str(self.datetime)[:19]
		self.date = self.dts[:10]
		self.time = self.dts[11:]

	def __repr__(self):
		return f"Snapshot ({self.hash}) on {self.date} at {self.time}"


