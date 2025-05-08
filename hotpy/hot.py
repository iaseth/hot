#!/usr/bin/env python3

import argparse

from pyhot.document import HotDocument



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

	parser.add_argument("--longest", action="store_true", help="Select the table with most rows")
	parser.add_argument("--widest", action="store_true", help="Select the table with most cols")
	parser.add_argument("--combine", action="store_true", help="Combine tables with same number of cols")

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
	parser.add_argument("--minc", type=int, default=None, help="Minimum table cols expected")
	parser.add_argument("--maxc", type=int, default=None, help="Maximum table cols expected")
	args = parser.parse_args()

	hotdoc = HotDocument(args)
	hotdoc.add_hot_tables_from_args()

	if hotdoc.empty:
		print("No tables found!")
		return

	hotdoc.post_processing()
	hotdoc.produce_output()


if __name__ == '__main__':
	main()
