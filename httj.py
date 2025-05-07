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


def filter_array(arr, s):
	if s is None:
		return arr
	elif is_int(s):
		index = int(s)
		return arr[:index]

	try:
		# Parse slice string
		parts = s.split(':')
		if len(parts) > 3:
			raise ValueError("Invalid slice format")
		slice_args = [int(p) if p else None for p in parts]
		return arr[slice(*slice_args)]
	except Exception as e:
		raise ValueError(f"Invalid filter string: {s}") from e


def get_row_cols(tr, cols_filter):
	cells = tr.find_all("th")
	if not cells:
		cells = tr.find_all("td")
	data = [cell.text.strip() for cell in cells]
	data = filter_array(data, cols_filter)
	return data


def get_table_data(table, args):
	thead = table.find("thead")
	tbody = table.find("tbody")

	if thead and tbody:
		headers = get_row_cols(thead.find('tr'), args.cols)
		tr_tags = tbody.find_all("tr")
	else:
		tr_tags = table.find_all("tr")
		headers = get_row_cols(tr_tags[0], args.cols)
		tr_tags = tr_tags[1:]

	rows = [get_row_cols(tr, args.cols) for tr in tr_tags]

	n_cols = len(rows[0])
	rows_are_uniform = all(len(row) == n_cols for row in rows)
	if rows_are_uniform:
		for n in range(n_cols):
			all_values_are_int = all(is_int(row[n]) for row in rows)
			all_values_are_float = all(is_float(row[n]) for row in rows)
			if all_values_are_int:
				for row in rows:
					row[n] = int(row[n])
			elif all_values_are_float:
				for row in rows:
					row[n] = float(row[n])

	if args.sort:
		rows = sorted(rows, key=lambda x:x[args.sort])

	if args.reverse:
		rows = reversed(rows)

	if args.rows:
		rows = filter_array(rows, args.rows)

	jo = {}
	jo["headers"] = headers
	jo["data"] = rows
	return jo


def get_tables_from_html(html: str, args):
	soup = BeautifulSoup(html, "lxml")
	table_tags = soup.find_all("table")
	if args.tables:
		table_tags = filter_array(table_tags, args.tables)

	tables = []
	for table_tag in table_tags:
		try:
			table = get_table_data(table_tag, args)
			tables.append(table)
		except Exception as e:
			print(e)
	return tables


def main():
	parser = argparse.ArgumentParser(description="Convert webpage tables to JSON table data.")
	parser.add_argument("url", nargs='?', help="URL of the webpage to extract tables from")
	parser.add_argument("-i", "--input", default=None, help="Optional input file")
	parser.add_argument("-o", "--output", default=None, help="Optional output file")

	parser.add_argument("-m", "--minified", action="store_true", help="Output JSON in minified format")
	parser.add_argument("-p", "--print", action="store_true", help="Print output in table format")
	parser.add_argument("-f", "--fmt", default="simple", help="Set table formatting")

	parser.add_argument("-r", "--rows", default=None, help="Filter rows")
	parser.add_argument("-c", "--cols", default=None, help="Filter columns")
	parser.add_argument("-t", "--tables", default=None, help="Filter tables")

	parser.add_argument("-s", "--sort", type=int, default=None, help="Sort table rows by nth column.")
	parser.add_argument("--reverse", action="store_true", help="Reverse table rows.")
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
