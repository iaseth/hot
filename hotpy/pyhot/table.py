from tabulate import tabulate

from .filter_list import filter_list



class HotTable:
	def __init__(self, document = None):
		self.document = document
		self.headers = []
		self.rows = []

	@property
	def values(self):
		return (self.headers, self.rows)

	@property
	def row_count(self):
		return len(self.rows)

	@property
	def col_count(self):
		return len(self.headers)

	@property
	def jo(self):
		table = {}
		table["headers"] = self.headers
		table["data"] = self.rows
		return table

	def is_acceptable(self, args):
		if args.min and self.row_count < args.min:
			return False
		elif args.max and self.row_count > args.max:
			return False
		elif args.minc and self.col_count < args.minc:
			return False
		elif args.maxc and self.col_count > args.maxc:
			return False
		return True

	def post_processing(self, args):
		if args.ascending:
			self.rows = sorted(self.rows, key=lambda x:x[args.ascending])
		elif args.descending:
			self.rows = sorted(self.rows, key=lambda x:x[args.descending], reverse=True)

		if args.reverse:
			self.rows.reverse()

		if args.r2:
			self.rows = filter_list(self.rows, args.r2)

		if args.c2:
			self.headers = filter_list(self.headers, args.c2)
			self.rows = [filter_list(row, args.c2) for row in self.rows]

		if args.id:
			self.headers = ["#", *self.headers]
			self.rows = [[i+1, *row] for i, row in enumerate(self.rows)]
		elif args.index:
			self.headers = ["#", *self.headers]
			self.rows = [[i, *row] for i, row in enumerate(self.rows)]
		elif args.uuid:
			headers = ["UUID", *headers]
			self.rows = [[str(uuid.uuid4()), *row] for row in self.rows]

	def print_table(self, args):
		table_text = tabulate(
			self.rows,
			headers=self.headers,
			tablefmt=args.fmt
		)
		print(table_text)

