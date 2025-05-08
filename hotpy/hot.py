#!/usr/bin/env python3

import argparse
import json
import os
import uuid

from bs4 import BeautifulSoup
from tabulate import tabulate

from pyhot.fetch import get_page_html
from pyhot.filter_list import filter_list
from pyhot.factory import create_table_from_table_tag



def get_table_data(table_tag, args):
	hot_table = create_table_from_table_tag(table_tag, args)
	hot_table.post_processing(args)
	return hot_table.values()


def get_tables_from_html(html: str, args):
	soup = BeautifulSoup(html, "lxml")
	table_tags = soup.find_all("table")
	table_tags = filter_list(table_tags, args.t1)

	tables = []
	for table_tag in table_tags:
		try:
			headers, rows = get_table_data(table_tag, args)
			if args.min and len(rows) < args.min:
				continue
			elif args.max and len(rows) > args.max:
				continue
			else:
				table = {}
				table["headers"] = headers
				table["data"] = rows
				tables.append(table)
		except Exception as e:
			print(e)

	tables = filter_list(tables, args.t2)
	return tables


def main():
	parser = argparse.ArgumentParser(description="Convert webpage tables to JSON table data.")
	parser.add_argument("url", nargs='?', help="URL of the webpage to extract tables from")
	parser.add_argument("-i", "--input", default=None, help="Optional input file")
	parser.add_argument("-o", "--output", default=None, help="Optional output file")

	parser.add_argument("--fetch", action="store_true", help="Fetch the page again, don't used cache")

	parser.add_argument("--csv", default=False, action="store_true", help="Output as CSV")
	parser.add_argument("--json", default=False, action="store_true", help="Output as JSON")
	parser.add_argument("--html", default=False, action="store_true", help="Output as HTML")
	parser.add_argument("--html5", default=False, action="store_true", help="Output as HTML5")
	parser.add_argument("--xml", default=False, action="store_true", help="Output as XML")
	parser.add_argument("--markdown", default=False, action="store_true", help="Output as Markdown")

	parser.add_argument("-m", "--minified", action="store_true", help="Output JSON in minified format")
	parser.add_argument("-p", "--print", action="store_true", help="Print output in table format")
	parser.add_argument("-f", "--fmt", default="simple", help="Set table formatting")

	parser.add_argument("--r1", default=None, help="Filter rows before processing")
	parser.add_argument("--c1", default=None, help="Filter columns before processing")
	parser.add_argument("--t1", default=None, help="Filter tables before processing")
	parser.add_argument("--r2", default=None, help="Filter rows after processing")
	parser.add_argument("--c2", default=None, help="Filter columns after processing")
	parser.add_argument("--t2", default=None, help="Filter tables after processing")

	parser.add_argument("-a", "--ascending", type=int, default=None, help="Sort table rows by nth column (ascending order)")
	parser.add_argument("-d", "--descending", type=int, default=None, help="Sort table rows by nth column (descending order)")
	parser.add_argument("-r", "--reverse", action="store_true", help="Reverse table rows")

	parser.add_argument("--id", default=False, action="store_true", help="Add id to table rows")
	parser.add_argument("--index", default=False, action="store_true", help="Add index to table rows")
	parser.add_argument("--uuid", default=False, action="store_true", help="Add uuid to table rows")

	parser.add_argument("--min", type=int, default=None, help="Minimum table rows expected")
	parser.add_argument("--max", type=int, default=None, help="Maximum table rows expected")
	args = parser.parse_args()

	if args.url:
		html = get_page_html(args.url, fetch=args.fetch)
	elif args.input:
		if os.path.isfile(args.input):
			with open(args.input) as f:
				html = f.read()
		else:
			print(f"File not found: '{args.input}'")
			return
	else:
		print(f"No URL of Input file provided!")
		return

	tables = get_tables_from_html(html, args)
	if len(tables) == 0:
		print("No tables found!")
		return

	if args.print:
		for table in tables:
			table_text = tabulate(
				table["data"],
				headers=table["headers"],
				tablefmt=args.fmt
			)
			print(table_text)
		return

	jo = {}
	jo["tables"] = tables
	json_text = json.dumps(
		jo, sort_keys = True, 
		indent=None if args.minified else "\t"
	)

	if args.output:
		with open(args.output, "w") as f:
			f.write(json_text)
		print(f"Saved: '{args.output}' ({len(tables)} tables)")
	else:
		print(json_text)


if __name__ == '__main__':
	main()
