import csv
import io
import random
import uuid

from tabulate import tabulate

from .evaluate import alphabet, alphabet_upper, evaluate_template
from .table_utils import camelize, get_snippet_args
from ..utils import filter_list
from ..utils import to_bool, to_int, to_float, to_str
from ..utils import strip_leading_dots, to_rounded
from ..utils import is_int, pop_first_value_between_xny



class HotTable:
	def __init__(self, document = None):
		self.document = document
		self.headers = []
		self.rows = []

	@property
	def values(self):
		return (self.headers, self.rows)

	def to_dataframe(self):
		df = pd.DataFrame(self.rows, columns=self.headers)
		return df

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
		if args.min_rows and self.row_count < args.min_rows: return False
		if args.max_rows and self.row_count > args.max_rows: return False
		if args.exact_rows and self.row_count != args.exact_rows: return False
		if args.min_cols and self.col_count < args.min_cols: return False
		if args.max_cols and self.col_count > args.max_cols: return False
		if args.exact_cols and self.col_count != args.exact_cols: return False
		return True

	def get_column_index(self, name, silent=False):
		if name == "":
			return None
		elif name.lower() in self.headers_lower:
			return self.headers_lower.index(name.lower())
		elif is_int(name):
			return int(name) % self.col_count
		elif len(name) == 1 and name in alphabet:
			return alphabet.index(name)
		elif len(name) == 1 and name in alphabet_upper:
			return self.col_count - (1 + alphabet_upper.index(name))
		else:
			if not silent:
				print(f"Column not found: '{name}'")
			return None

	def get_column_indexes(self, args, separator=",", silent=False):
		column_names = separator.join(args).split(separator)
		column_indexes = [self.get_column_index(name, silent=silent) for name in column_names]
		column_indexes = [idx for idx in column_indexes if idx != None]
		column_indexes = [idx for idx in column_indexes if abs(idx) < self.col_count]
		return column_indexes

	def perform_c1_r1_filtering(self):
		# used by non-HTML factories
		self.rows = filter_list(self.rows, self.args.r1)
		if self.args.c1:
			self.headers = filter_list(self.headers, self.args.c1)
			self.rows = [filter_list(row, self.args.c1) for row in self.rows]

	def process_template_args(self, args):
		for arg in args:
			parts = arg.split("=")
			if len(parts) == 2:
				header, template = parts
			else:
				header, template = ("@", arg)
			self.headers = [*self.headers, header]
			self.rows = [[*row, evaluate_template(template, row)] for row in self.rows]

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

	def print_table(self, n=10, fmt="simple"):
		table_text = tabulate(
			self.rows[:n],
			headers=self.headers,
			tablefmt=fmt
		)
		print(table_text)
		if n < self.row_count:
			print(f"({self.row_count-n} more rows in table)")

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

	def round_columns_to_n_digits(self, args):
		if not args: return None
		for arg in args:
			digits, col_arg = strip_leading_dots(arg)
			col_indexes = self.get_column_indexes([col_arg])

			for row in self.rows:
				for col_index in col_indexes:
					row[col_index] = to_rounded(row[col_index], digits)


	def sort_rows(self, arg, reverse=False):
		cdx = self.get_column_index(arg)
		if cdx is None:
			print(f"Invalid column for sorting: '{arg}'")
			return
		self.rows = sorted(self.rows, key=lambda x:x[cdx], reverse=reverse)


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

	def move_columns(self, arg):
		pass

	def swap_two_columns(self, arg):
		column_indexes = self.get_column_indexes([arg], separator=":")
		if len(column_indexes) != 2:
			print(f"Bad swap arg: '{arg}'")
			return

		c1, c2 = column_indexes
		def swap(arr):
			arr[c1], arr[c2] = arr[c2], arr[c1]
		swap(self.headers)
		for row in self.rows:
			swap(row)

	def extract_column_between_parens(self, arg):
		self.extract_column_between_xny(arg, start_char='(', end_char=')')

	def extract_column_between_braces(self, arg):
		self.extract_column_between_xny(arg, start_char='{', end_char='}')

	def extract_column_between_brackets(self, arg):
		self.extract_column_between_xny(arg, start_char='[', end_char=']')

	def extract_column_between_xny(self, arg, start_char, end_char):
		header = "New"
		eq_idx = arg.find("=")
		if eq_idx != -1:
			header = arg[eq_idx+1:]
			arg = arg[:eq_idx]

		cdx = self.get_column_index(arg)
		if cdx is None: return
		if cdx >= self.col_count: return

		self.headers.insert(cdx+1, header)
		for row in self.rows:
			c1, c2 = pop_first_value_between_xny(row[cdx], start_char=start_char, end_char=end_char)
			row[cdx] = c1
			row.insert(cdx+1, c2)


	def min_max_filtering(self, args, max=False):
		if not args: return
		for arg in args:
			try:
				col_index, value = arg.split("=")
				col_index = self.get_column_index(col_index)
				value = to_float(value)
				if max:
					self.rows = [row for row in self.rows if row[col_index] <= value]
				else:
					self.rows = [row for row in self.rows if row[col_index] >= value]
			except:
				print(f"Invalid min/max arg: '{arg}'")


	def select_random_rows(self, n, preserve_order=False):
		indices = random.sample(range(self.row_count), n)
		if preserve_order:
			indices = sorted(indices)
		self.rows = [self.rows[i] for i in indices]

	def mirror_table(self):
		self.headers = reversed(self.headers)
		self.rows = [reversed(row) for row in self.rows]

	def snip_table(self, arg):
		snip_args = get_snippet_args(arg)
		if not snip_args:
			print(f"Bad snippet arg: '{arg}'")
			return

		c1, r1, c2, r2 = snip_args
		self.rows = self.rows[r1-1:r2]

		self.headers = self.headers[c1:c2+1]
		self.rows = [row[c1:c2+1] for row in self.rows]

	def transpose_table(self):
		total_rows = [self.headers, *self.rows]
		def get_nth_column(rows, n):
			return [row[n] for row in rows]

		headers = get_nth_column(total_rows, 0)
		rows = [get_nth_column(total_rows, i) for i in range(1, self.col_count)]
		self.headers = headers
		self.rows = rows


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
		return f"HotTable ({self.row_count} x {self.col_count})"

