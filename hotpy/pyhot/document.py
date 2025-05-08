import json
import os

from bs4 import BeautifulSoup

from .fetch import get_page_html
from .filter_list import filter_list
from .table import HotTable
from .factory import create_table_from_table_tag



class HotDocument:
	def __init__(self, args):
		self.args = args
		self.tables = []

	def add_hot_tables_from_args(self):
		if not self.args.url and not self.args.input:
			print(f"No URL of Input file provided!")
			return

		if self.args.url:
			html = get_page_html(self.args.url, fetch=self.args.fetch)
			self.add_hot_tables_from_html(html)

		if self.args.input:
			if os.path.isfile(self.args.input):
				with open(self.args.input) as f:
					html = f.read()
				self.add_hot_tables_from_html(html)
			else:
				print(f"File not found: '{self.args.input}'")
				return

	def add_hot_tables_from_html(self, html: str):
		soup = BeautifulSoup(html, "lxml")
		table_tags = soup.find_all("table")
		table_tags = filter_list(table_tags, self.args.t1)

		for table_tag in table_tags:
			try:
				table = create_table_from_table_tag(self, table_tag)
				if table.is_acceptable():
					self.tables.append(table)
			except Exception as e:
				print(e)

		self.tables = filter_list(self.tables, self.args.t2)

	def longest_tables(self):
		n = max(t.row_count for t in self.tables)
		return [t for t in self.tables if t.row_count == n]

	def widest_tables(self):
		n = max(t.col_count for t in self.tables)
		return [t for t in self.tables if t.col_count == n]

	def post_processing(self):
		if self.args.longest:
			self.tables = self.longest_tables()

		if self.args.widest:
			self.tables = self.widest_tables()

		if self.args.combine:
			col_counts = set(t.col_count for t in self.tables)
			combined_tables = []
			for col_count in col_counts:
				matching_tables = [t for t in self.tables if t.col_count == col_count]
				combined_table = sum(matching_tables[1:], matching_tables[0])
				combined_tables.append(combined_table)
			self.tables = combined_tables
		elif self.args.join:
			row_counts = set(t.row_count for t in self.tables)
			joined_tables = []
			for row_count in row_counts:
				matching_tables = [t for t in self.tables if t.row_count == row_count]
				joined_table = matching_tables[0]
				for table in matching_tables[1:]:
					joined_table = joined_table.join(table)
				joined_tables.append(joined_table)
			self.tables = joined_tables

		for table in self.tables:
			table.post_processing()

	def print_summary(self):
		for table in self.tables:
			print(table)

	def print_tables(self):
		for table in self.tables:
			table.print_table()
			print()

	def produce_output(self):
		if self.args.summary:
			self.print_summary()
		elif self.args.print:
			self.print_tables()
		elif self.args.output:
			with open(self.args.output, "w") as f:
				f.write(self.json_text)
			print(f"Saved: '{self.args.output}' ({len(self.tables)} tables)")
		else:
			print(self.json_text)

	@property
	def empty(self):
		return len(self.tables) == 0

	@property
	def table_count(self):
		return len(self.tables)

	@property
	def jo(self):
		jo = {}
		if self.args.flat and self.table_count == 1:
			jo["table"] = self.tables[0].jo
		elif self.args.naked and self.table_count == 1:
			jo = self.tables[0].jo
		else:
			jo["tables"] = [table.jo for table in self.tables]
		return jo

	@property
	def indent(self):
		if self.args.minified:
			return None
		elif self.args.s2:
			return 2
		elif self.args.s4:
			return 4
		else:
			return "\t"

	@property
	def json_text(self):
		json_text = json.dumps(
			self.jo, sort_keys = True, 
			indent=self.indent
		)
		return json_text


