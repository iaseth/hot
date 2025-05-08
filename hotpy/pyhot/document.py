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


