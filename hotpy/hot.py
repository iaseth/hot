#!/usr/bin/env python3

import argparse

from pyhot.document import HotDocument



def main():
	parser = argparse.ArgumentParser(description="Convert webpage tables to JSON table data.")
	parser.add_argument("--cache", action="store_true", help="Cache any fetch requests")
	parser.add_argument("--fetch", action="store_true", help="Fetch the page again, don't use cache")

	parser.add_argument("-x", "--cut", action="store_true", help="Put output into clipboard")
	parser.add_argument("-c", "--copy", action="store_true", help="Copy output to clipboard")
	parser.add_argument("-v", "--paste", action="store_true", help="Take input HTML from clipboard")
	parser.add_argument("--paste-path", action="store_true", help="Take input path from clipboard")

	parser.add_argument("-o", "--output", default=None, help="Optional output file")
	parser.add_argument("--csv", default=False, action="store_true", help="Output as CSV")
	parser.add_argument("--html", default=False, action="store_true", help="Output as HTML")
	parser.add_argument("--html5", default=False, action="store_true", help="Output as HTML5")
	parser.add_argument("--json", default=False, action="store_true", help="Output as JSON")
	parser.add_argument("--markdown", default=False, action="store_true", help="Output as Markdown")
	parser.add_argument("--xml", default=False, action="store_true", help="Output as XML")

	parser.add_argument("-m", "--minified", action="store_true", help="Output JSON in minified format")
	parser.add_argument("--s2", action="store_true", help="Indent JSON with 2 spaces")
	parser.add_argument("--s4", action="store_true", help="Indent JSON with 4 spaces")
	parser.add_argument("--flat", action="store_true", help="Output flat JSON if single table")
	parser.add_argument("--naked", action="store_true", help="Output naked JSON if single table")
	parser.add_argument("--obj", action="store_true", help="Output rows as objects in JSON")

	parser.add_argument("--fmt", default="simple", help="Set table formatting")
	parser.add_argument("-s", "--summary", action="store_true", help="Print output in summary format")

	parser.add_argument("--longest", action="store_true", help="Select the table with most rows")
	parser.add_argument("--widest", action="store_true", help="Select the table with most cols")
	parser.add_argument("-j", "--join", action="store_true", help="Join tables with same number of rows")
	parser.add_argument("-u", "--union", action="store_true", help="Combine tables with same number of cols")

	parser.add_argument("--r1", default=None, help="Filter rows before processing")
	parser.add_argument("--c1", default=None, help="Filter columns before processing")
	parser.add_argument("--t1", default=None, help="Filter tables before processing")
	parser.add_argument("--r2", default=None, help="Filter rows after processing")
	parser.add_argument("--c2", default=None, help="Filter columns after processing")
	parser.add_argument("--t2", default=None, help="Filter tables after processing")

	parser.add_argument("-t", "--template", nargs='+', help="Add a template column")
	parser.add_argument("-f", "--filter", nargs='+', help="Filter rows by condition")

	parser.add_argument("--bool", nargs='+', help="Convert column values to boolean")
	parser.add_argument("--int", nargs='+', help="Convert column values to int")
	parser.add_argument("--float", nargs='+', help="Convert column values to float")
	parser.add_argument("--str", nargs='+', help="Convert column values to string")

	parser.add_argument("--drop", nargs='+', help="Drop certain columns")
	parser.add_argument("--keep", nargs='+', help="Keep certain columns")
	parser.add_argument("--min", nargs='+', help="Filter rows by minimum value for column")
	parser.add_argument("--max", nargs='+', help="Filter rows by maximum value for column")

	parser.add_argument("-a", "--ascending", type=int, default=None, help="Sort table rows by nth column (ascending order)")
	parser.add_argument("-d", "--descending", type=int, default=None, help="Sort table rows by nth column (descending order)")
	parser.add_argument("-r", "--reverse", action="store_true", help="Reverse table rows order")

	parser.add_argument("--id", default=False, action="store_true", help="Add id to table rows")
	parser.add_argument("--index", default=False, action="store_true", help="Add index to table rows")
	parser.add_argument("--uuid", default=False, action="store_true", help="Add uuid to table rows")

	parser.add_argument("--minr", type=int, default=None, help="Minimum table rows expected")
	parser.add_argument("--maxr", type=int, default=None, help="Maximum table rows expected")
	parser.add_argument("--exact", type=int, default=None, help="Exact number of table rows expected")
	parser.add_argument("--minc", type=int, default=None, help="Minimum table cols expected")
	parser.add_argument("--maxc", type=int, default=None, help="Maximum table cols expected")
	parser.add_argument("--exactc", type=int, default=None, help="Exact number of table cols expected")

	args, input_paths = parser.parse_known_args()
	hotdoc = HotDocument(args)
	hotdoc.add_hot_tables_from_args(input_paths)

	if hotdoc.empty:
		print("No tables found!")
		return

	hotdoc.post_processing()
	hotdoc.produce_output()


if __name__ == '__main__':
	main()
