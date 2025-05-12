from .snapshot import Snapshot



class TimeMachine:
	def __init__(self, hotdoc):
		self.hotdoc = hotdoc
		self.snapshots = []

	def snap(self):
		if self.snapshots and self.snapshots[-1].hash == self.hotdoc.hash:
			print(f"Snapshots up-to-date: {self.snapshots[-1]}")
			return

		snapshot = Snapshot(self)
		self.snapshots.append(snapshot)
		print(f"Took a snapshot: {snapshot}")

	def forget(self):
		print(f"Forgot {len(self.snapshots)} snapshots!")
		self.snapshots = []

	def history(self):
		print(f"Found {len(self.snapshots)} snapshots!")
		for i, snapshot in enumerate(self.snapshots, start=1):
			print(f"\t{i:2}/{len(self.snapshots):02}. {snapshot}")

	def undo(self):
		if not self.snapshots:
			print(f"No snapshots to undo to!")
			return

		snapshot = self.snapshots.pop()
		self.hotdoc.empty_document()
		self.hotdoc.add_hot_tables_from_json_text(snapshot.json_text)
		print(f"Did undo to: {snapshot}!")

	def redo(self):
		print(f"Redo command not implemented!")


