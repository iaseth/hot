import uuid

from tabulate import tabulate

from .filter_list import filter_list
from .table_utils import camelize



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
	def camel_headers(self):
		return [camelize(h) for h in self.headers]

	def make_row_object(self, row, headers=None):
		headers = headers or self.headers
		row_object = { h: v for h, v in zip(headers, row) }
		return row_object

	@property
	def args(self):
		return self.document.args

	def has_unique_column_names(self):
		if not all(self.headers):
			return False
		return len(set(self.headers)) == len(self.headers)

	@property
	def jo(self):
		table = {}
		table["headers"] = self.headers
		if self.args.obj and self.has_unique_column_names():
			camel_headers = self.camel_headers
			table["data"] = [self.make_row_object(row, headers=camel_headers) for row in self.rows]
		else:
			table["data"] = self.rows
		return table

	def is_acceptable(self):
		args = self.args
		if args.min and self.row_count < args.min: return False
		if args.max and self.row_count > args.max: return False
		if args.exact and self.row_count != args.exact: return False
		if args.minc and self.col_count < args.minc: return False
		if args.maxc and self.col_count > args.maxc: return False
		if args.exactc and self.col_count != args.exactc: return False
		return True

	def post_processing(self):
		args = self.args
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
			self.headers = ["UUID", *self.headers]
			self.rows = [[str(uuid.uuid4()), *row] for row in self.rows]

	def print_table(self):
		table_text = tabulate(
			self.rows,
			headers=self.headers,
			tablefmt=self.args.fmt
		)
		print(table_text)

	def __add__(self, other):
		result = HotTable(self.document)
		result.headers = self.headers
		result.rows = [*self.rows, *other.rows]
		return result

	def __repr__(self):
		return f"HotTable ({self.col_count} cols, {self.row_count} rows)"

