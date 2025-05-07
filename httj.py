#!/usr/bin/env python3

import argparse
import json
import os

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


DEFAULT_HEADERS = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
	# "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	# "Accept-Language": "en-US,en;q=0.9",
	# "Connection": "keep-alive",
	# "Cache-Control": "no-cache",
	# "Pragma": "no-cache",
}


def is_int(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def is_float(s):
	try:
		float(s)
		return True
	except ValueError:
		return False


def get_row_cols(tr, n_cols=0):
	cells = tr.find_all("th")
	if not cells:
		cells = tr.find_all("td")
	data = [cell.text.strip() for cell in cells]
	if n_cols:
		data = data[:n_cols]
	return data


def get_table_data(table, args):
	thead = table.find("thead")
	tbody = table.find("tbody")

	headers = get_row_cols(thead.find('tr'), args.cols)
	tr_tags = tbody.find_all("tr")
	if args.rows:
		tr_tags = tr_tags[:args.rows]
	data = [get_row_cols(tr, args.cols) for tr in tr_tags]

	n_cols = len(data[0])
	rows_are_uniform = all(len(row) == n_cols for row in data)
	if rows_are_uniform:
		for n in range(n_cols):
			all_values_are_int = all(is_int(row[n]) for row in data)
			all_values_are_float = all(is_float(row[n]) for row in data)
			if all_values_are_int:
				for row in data:
					row[n] = int(row[n])
			elif all_values_are_float:
				for row in data:
					row[n] = float(row[n])

	jo = {}
	jo["headers"] = headers
	jo["data"] = data
	return jo


def get_tables_from_html(html: str, args):
	soup = BeautifulSoup(html, "lxml")
	table_tags = soup.find_all("table")
	if args.tables:
		table_tags = table_tags[:args.tables]

	tables = []
	for table_tag in table_tags:
		try:
			table = get_table_data(table_tag, args)
			tables.append(table)
		except Exception as e:
			pass
	return tables


def main():
	parser = argparse.ArgumentParser(description="Convert webpage tables to JSON table data.")
	parser.add_argument("url", nargs='?', help="URL of the webpage to extract tables from")
	parser.add_argument("-i", "--input", default=None, help="Optional input file")
	parser.add_argument("-o", "--output", default=None, help="Optional output file")

	parser.add_argument("-m", "--minified", action="store_true", help="Output JSON in minified format")
	parser.add_argument("-p", "--print", action="store_true", help="Print output in table format")
	parser.add_argument("-f", "--fmt", default="simple", help="Set table formatting")

	parser.add_argument("-r", "--rows", type=int, default=None, help="Number of Rows")
	parser.add_argument("-c", "--cols", type=int, default=None, help="Number of Columns")
	parser.add_argument("-t", "--tables", type=int, default=None, help="Number of Tables")
	args = parser.parse_args()

	if args.url:
		response = requests.get(args.url, headers=DEFAULT_HEADERS)
		html = response.text
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
	if args.minified:
		json_text = json.dumps(tables, sort_keys=True)
	else:
		json_text = json.dumps(tables, sort_keys=True, indent="\t")

	if args.output:
		with open(args.output, "w") as f:
			f.write(json_text)
		print(f"Saved: '{args.output}' ({len(tables)} tables)")
	else:
		print(json_text)


if __name__ == '__main__':
	main()
