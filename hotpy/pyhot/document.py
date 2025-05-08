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
				table = create_table_from_table_tag(table_tag, self.args)
				if table.is_acceptable(self.args):
					self.tables.append(table)
			except Exception as e:
				print(e)

		self.tables = filter_list(self.tables, self.args.t2)

	def post_processing(self):
		if self.args.combine:
			col_counts = set(t.col_count for t in self.tables)
			combined_tables = []
			for col_count in col_counts:
				matching_tables = [t for t in self.tables if t.col_count == col_count]
				combined_table = sum(matching_tables[1:], matching_tables[0])
				combined_tables.append(combined_table)
			self.tables = combined_tables

		for table in self.tables:
			table.post_processing(self.args)

	@property
	def jo(self):
		jo = {}
		jo["tables"] = [table.jo for table in self.tables]
		return jo

	@property
	def json_text(self):
		json_text = json.dumps(
			self.jo, sort_keys = True, 
			indent=None if self.args.minified else "\t"
		)
		return json_text


