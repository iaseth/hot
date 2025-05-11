import json
import os

from bs4 import BeautifulSoup
import pyperclip

from .factory import create_table_from_table_tag, create_table_from_jo, create_table_from_csv
from .fetch import get_page_html
from .filter_list import filter_list
from .output import document_to_html5, document_to_html, document_to_xml
from .table import HotTable



class HotDocument:
	def __init__(self, args):
		self.args = args
		self.tables = []

	def add_hot_tables_from_args(self, input_paths):
		if self.args.paste:
			html = pyperclip.paste()
			self.add_hot_tables_from_html(html)

		if self.args.paste_path:
			path_in_clipboard = pyperclip.paste()
			input_paths.append(path_in_clipboard)

		for input_path in input_paths:
			if os.path.isfile(input_path):
				self.add_hot_tables_from_file(input_path)
			elif input_path.startswith("-"):
				print(f"Unknown flag: '{input_path}'")
			elif "." in input_path:
				html = get_page_html(input_path, fetch=self.args.fetch, cache=self.args.cache)
				self.add_hot_tables_from_html(html)
			else:
				print(f"File not found: '{input_path}'")
				return

		self.tables = filter_list(self.tables, self.args.t2)

	def add_hot_tables_from_file(self, input_path: str):
		if input_path.endswith(".csv"):
			self.add_hot_tables_from_csv_file(input_path)
		elif input_path.endswith(".json"):
			self.add_hot_tables_from_json_file(input_path)
		else:
			with open(input_path) as f:
				html = f.read()
			self.add_hot_tables_from_html(html)

	def add_hot_tables_from_csv_file(self, input_path):
		table = create_table_from_csv(self, input_path)
		if table and table.is_acceptable():
			self.tables.append(table)

	def add_hot_tables_from_json_file(self, json_path):
		with open(json_path) as f:
			jo = json.load(f)
		if not "tables" in jo: return

		for table_jo in jo["tables"]:
			try:
				table = create_table_from_jo(self, table_jo)
				if table.is_acceptable():
					self.tables.append(table)
			except Exception as e:
				print(e)

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

	def longest_tables(self):
		n = max(t.row_count for t in self.tables)
		return [t for t in self.tables if t.row_count == n]

	def widest_tables(self):
		n = max(t.col_count for t in self.tables)
		return [t for t in self.tables if t.col_count == n]

	def union_tables(self):
		col_counts = set(t.col_count for t in self.tables)
		combined_tables = []
		for col_count in col_counts:
			matching_tables = [t for t in self.tables if t.col_count == col_count]
			combined_table = sum(matching_tables[1:], matching_tables[0])
			combined_tables.append(combined_table)
		self.tables = combined_tables

	def join_tables(self):
		row_counts = set(t.row_count for t in self.tables)
		joined_tables = []
		for row_count in row_counts:
			matching_tables = [t for t in self.tables if t.row_count == row_count]
			joined_table = matching_tables[0]
			for table in matching_tables[1:]:
				joined_table = joined_table.join(table)
			joined_tables.append(joined_table)
		self.tables = joined_tables

	def print_summary(self):
		for table in self.tables:
			print(table)

	def get_output_text(self):
		if self.args.json:
			return self.json_text
		elif self.args.html5:
			return document_to_html5(self)
		elif self.args.html:
			return document_to_html(self)
		elif self.args.xml:
			return document_to_xml(self)
		else:
			return "\n".join([t.get_output_text() for t in self.tables])

	def produce_output(self):
		if self.args.summary:
			self.print_summary()
			return

		output_text = self.get_output_text()
		if self.args.cut:
			pyperclip.copy(output_text)
			print(f"Put output into clipboard.")
			return
		elif self.args.copy:
			pyperclip.copy(output_text)
			print(f"Copied output to clipboard.")

		if self.args.output:
			with open(self.args.output, "w") as f:
				f.write(output_text)
			print(f"Saved: '{self.args.output}' ({len(self.tables)} tables)")
		else:
			print(output_text)

	@property
	def is_empty(self):
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
		if self.args.tabs:
			return "\t"
		elif self.args.s2:
			return 2
		elif self.args.s4:
			return 4
		elif self.args.minified:
			return None
		else:
			return None

	@property
	def space(self):
		if self.args.minified:
			return ""
		elif self.args.s2:
			return " " * 2
		elif self.args.s4:
			return " " * 4
		else:
			return "\t"

	@property
	def json_text(self):
		json_text = json.dumps(
			self.jo, sort_keys = True, 
			indent=self.indent
		)
		return json_text


