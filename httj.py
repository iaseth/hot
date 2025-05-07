#!/usr/bin/env python3

import argparse
import json
import os

from bs4 import BeautifulSoup


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


def get_row_cols(tr):
	cells = tr.find_all("th")
	if not cells:
		cells = tr.find_all("td")
	data = [cell.text.strip() for cell in cells]
	return data


def get_table_data(table):
	thead = table.find("thead")
	tbody = table.find("tbody")

	headers = get_row_cols(thead.find('tr'))
	data = [get_row_cols(tr) for tr in tbody.find_all("tr")]

	n_cols = len(data[0])
	rows_are_uniform = all(len(row) == n_cols for row in data)
	if rows_are_uniform:
		for n in range(n_cols):
			all_values_are_int = all(is_int(row[n]) for row in data)
			if all_values_are_int:
				for row in data:
					row[n] = int(row[n])

			all_values_are_float = all(is_float(row[n]) for row in data)
			if all_values_are_float:
				for row in data:
					row[n] = float(row[n])

	jo = {}
	jo["headers"] = headers
	jo["data"] = data
	return jo


def get_tables_from_html(html: str):
	soup = BeautifulSoup(html, "lxml")
	tables = [get_table_data(table) for table in soup.find_all("table")]
	return tables


def main():
	parser = argparse.ArgumentParser(description="Convert webpage tables to JSON table data.")
	parser.add_argument("url", nargs='?', help="URL of the webpage to extract tables from")
	parser.add_argument("-i", "--input", default=None, help="Optional input file")
	parser.add_argument("-o", "--output", default=None, help="Optional output file")
	parser.add_argument("-m", "--minified", action="store_true", help="Output JSON in minified format")
	parser.add_argument("-n", "--number", type=int, default=None, help="Optional number parameter (e.g., limit number of tables)")
	args = parser.parse_args()

	if args.url:
		response = requests.get(args.url)
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

	tables = get_tables_from_html(html)

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
