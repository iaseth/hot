import csv
import io
import uuid

from tabulate import tabulate

from .convert_utils import to_bool, to_int, to_float, to_str
from .evaluate import alphabet, alphabet_upper, evaluate_template
from .filter_list import filter_list
from .number_utils import is_int
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
	def headers_lower(self):
		return [h.lower() for h in self.headers]

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
		if self.args.obj and self.has_unique_column_names():
			camel_headers = self.camel_headers
			table["headers"] = self.make_row_object(self.headers, headers=camel_headers)
			table["data"] = [self.make_row_object(row, headers=camel_headers) for row in self.rows]
		else:
			table["headers"] = self.headers
			table["data"] = self.rows
		return table

	def is_acceptable(self):
		args = self.args
		if args.minr and self.row_count < args.minr: return False
		if args.maxr and self.row_count > args.maxr: return False
		if args.exact and self.row_count != args.exact: return False
		if args.minc and self.col_count < args.minc: return False
		if args.maxc and self.col_count > args.maxc: return False
		if args.exactc and self.col_count != args.exactc: return False
		return True

	def get_column_index(self, name):
		if name.lower() in self.headers_lower:
			return self.headers_lower.index(name.lower())
		elif is_int(name):
			return int(name)
		elif len(name) == 1 and name in alphabet:
			return alphabet.index(name)
		elif len(name) == 1 and name in alphabet_upper:
			return self.col_count - (1 + alphabet_upper.index(name))
		else:
			print(f"Column not found: '{name}'")
			return None

	def get_column_indexes(self, args):
		column_names = ",".join(args).split(",")
		column_indexes = [self.get_column_index(name) for name in column_names]
		column_indexes = [idx for idx in column_indexes if idx != None]
		column_indexes = [idx for idx in column_indexes if abs(idx) < self.col_count]
		return column_indexes

	def post_processing(self):
		args = self.args
		self.perform_conversions()
		self.perform_scaling()
		self.add_template_columns()
		self.perform_ordering()
		self.perform_filtering()
		self.add_indexes()

	def perform_conversions(self):
		self.convert_columns_to_x(self.args.bool, to_bool)
		self.convert_columns_to_x(self.args.int, to_int)
		self.convert_columns_to_x(self.args.float, to_float)
		self.convert_columns_to_x(self.args.str, to_str)
		if self.args.shave:
			self.shave_headers()

	def perform_scaling(self):
		self.scale_columns(self.args.kilo, divisor=1000)
		self.scale_columns(self.args.mega, divisor=1000_000)
		self.scale_columns(self.args.giga, divisor=1000_000_000)
		self.scale_columns(self.args.centi, multiplier=100)
		self.scale_columns(self.args.milli, multiplier=1000)
		self.scale_columns(self.args.micro, multiplier=1000_000)
		self.scale_columns(self.args.nano, multiplier=1000_000_000)

	def add_template_columns(self):
		if self.args.template:
			for arg in self.args.template:
				parts = arg.split("=")
				if len(parts) == 2:
					header, template = parts
				else:
					header, template = ("@", arg)
				self.headers = [*self.headers, header]
				self.rows = [[*row, evaluate_template(template, row)] for row in self.rows]

	def perform_ordering(self):
		if self.args.ascending:
			col_index = self.get_column_index(self.args.ascending)
			self.rows = sorted(self.rows, key=lambda x:x[col_index])
		elif self.args.descending:
			col_index = self.get_column_index(self.args.descending)
			self.rows = sorted(self.rows, key=lambda x:x[col_index], reverse=True)

		if self.args.reverse:
			self.rows.reverse()

	def perform_filtering(self):
		args = self.args
		if args.drop:
			col_indexes = self.get_column_indexes(args.drop)
			self.drop_certain_columns(col_indexes)

		if args.keep:
			col_indexes = self.get_column_indexes(args.keep)
			self.keep_certain_columns(col_indexes)

		if args.max:
			for max_value in args.max:
				try:
					col_index, value = [int(x) for x in max_value.split("=")]
					self.rows = [row for row in self.rows if row[col_index] < value]
				except:
					print(f"Invalid max arg: '{max_value}'")

		if args.min:
			for min_value in args.min:
				try:
					col_index, value = [int(x) for x in min_value.split("=")]
					self.rows = [row for row in self.rows if row[col_index] > value]
				except:
					print(f"Invalid min arg: '{min_value}'")

		if args.r2:
			self.rows = filter_list(self.rows, args.r2)

		if args.c2:
			self.headers = filter_list(self.headers, args.c2)
			self.rows = [filter_list(row, args.c2) for row in self.rows]

	def add_indexes(self):
		if self.args.id:
			self.headers = ["Id", *self.headers]
			self.rows = [[i+1, *row] for i, row in enumerate(self.rows)]
		elif self.args.index:
			self.headers = ["Index", *self.headers]
			self.rows = [[i, *row] for i, row in enumerate(self.rows)]
		elif self.args.uuid:
			self.headers = ["UUID", *self.headers]
			self.rows = [[str(uuid.uuid4()), *row] for row in self.rows]


	def shave_headers(self):
		self.headers = [header.split(" ")[0] for header in self.headers]


	def get_tabulate(self):
		table_text = tabulate(
			self.rows,
			headers=self.headers,
			tablefmt=self.args.fmt
		)
		return table_text

	def print_tabulate(self):
		print(self.get_tabulate())

	def join(self, other):
		result = HotTable(self.document)
		result.headers = [*self.headers, *other.headers]
		result.rows = [[*r1, *r2] for r1, r2 in zip(self.rows, other.rows)]
		return result


	def convert_columns_to_x(self, args, to_x):
		if not args: return None
		col_indexes = self.get_column_indexes(args)
		for row in self.rows:
			for col_index in col_indexes:
				row[col_index] = to_x(row[col_index])


	def scale_columns(self, args, divisor=0, multiplier=0):
		if not args: return None
		col_indexes = self.get_column_indexes(args)
		for row in self.rows:
			for col_index in col_indexes:
				if divisor:
					row[col_index] = row[col_index] // divisor
				elif multiplier:
					row[col_index] = int(row[col_index] * multiplier)


	def drop_certain_columns(self, col_indexes):
		def drop_filter(arr):
			return [x for i, x in enumerate(arr) if not i in col_indexes]
		self.headers = drop_filter(self.headers)
		self.rows = [drop_filter(row) for row in self.rows]

	def keep_certain_columns(self, col_indexes):
		def keep_filter(arr):
			return [x for i, x in enumerate(arr) if i in col_indexes]
		self.headers = keep_filter(self.headers)
		self.rows = [keep_filter(row) for row in self.rows]


	def to_csv(self):
		output = io.StringIO()
		writer = csv.writer(output)
		writer.writerow(self.headers)
		writer.writerows(self.rows)
		return output.getvalue()

	def to_markdown(self):
		return tabulate(self.rows, headers=self.headers, tablefmt="github")

	def get_output_text(self):
		if self.args.csv:
			return self.to_csv()
		elif self.args.markdown:
			return self.to_markdown()
		else:
			return self.get_tabulate()


	def __add__(self, other):
		result = HotTable(self.document)
		result.headers = self.headers
		result.rows = [*self.rows, *other.rows]
		return result

	def __repr__(self):
		return f"HotTable ({self.col_count} cols, {self.row_count} rows)"

