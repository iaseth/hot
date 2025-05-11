import time
import uuid

from .hotparse import HotFlag
from .utils import filter_list_by_args, strip_leading_dots
from .utils import to_bool, to_int, to_float, to_str, to_rounded
from .utils import format_duration_ns



def manipulate_table(table, flag):
	manipulator = flag.flag
	hotargs = flag.args
	args = flag.string_args

	first_arg = args[0] if args else None
	column_indexes = table.get_column_indexes(args, silent=True)

	match manipulator:
		# index addition stuff
		case "--id":
			table.headers = ["Id", *table.headers]
			table.rows = [[i+1, *row] for i, row in enumerate(table.rows)]
		case "--index":
			table.headers = ["Index", *table.headers]
			table.rows = [[i, *row] for i, row in enumerate(table.rows)]
		case "--uuid":
			table.headers = ["UUID", *table.headers]
			table.rows = [[str(uuid.uuid4()), *row] for row in table.rows]

		# conversion stuff
		case "--bool": table.convert_columns_to_x(args, to_bool)
		case "--int": table.convert_columns_to_x(args, to_int)
		case "--float": table.convert_columns_to_x(args, to_float)

		case "--str": table.convert_columns_to_x(args, to_str)
		case "--lower": table.convert_columns_to_x(args, str.lower)
		case "--upper": table.convert_columns_to_x(args, str.upper)
		case "--strip": table.convert_columns_to_x(args, str.strip)
		case "--lstrip": table.convert_columns_to_x(args, str.lstrip)
		case "--rstrip": table.convert_columns_to_x(args, str.rstrip)
		case "--shave": table.shave_headers(args)

		# scaling stuff
		case "--kilo": table.scale_columns(args, divisor=1000)
		case "--mega": table.scale_columns(args, divisor=1000_000)
		case "--giga": table.scale_columns(args, divisor=1000_000_000)
		case "--centi": table.scale_columns(args, multiplier=100)
		case "--milli": table.scale_columns(args, multiplier=1000)
		case "--micro": table.scale_columns(args, multiplier=1000_000)
		case "--nano": table.scale_columns(args, multiplier=1000_000_000)

		case "-t" | "--template": table.process_template_args(args)
		case "--round": table.round_columns_to_n_digits(args)

		# ordering stuff
		case "-a" | "--ascending": table.sort_rows(first_arg)
		case "-d" | "--descending": table.sort_rows(first_arg, reverse=True)
		case "-R" | "--reverse": table.rows.reverse()

		# filtering stuff
		case "-r" | "--rows":
			table.rows = filter_list_by_args(table.rows, args)

		case "-c" |  "--cols":
			table.headers = filter_list_by_args(table.headers, args)
			table.rows = [filter_list_by_args(row, args) for row in table.rows]

		case "--drop": table.drop_certain_columns(column_indexes)
		case "--keep": table.keep_certain_columns(column_indexes)
		case "--move": flag.forEachArg(table.move_columns)
		case "--swap": flag.forEachArg(table.swap_two_columns)

		# undocumented
		case "--parens": flag.forEachArg(table.extract_column_between_parens)
		case "--braces": flag.forEachArg(table.extract_column_between_braces)
		case "--brackets": flag.forEachArg(table.extract_column_between_brackets)

		case "--min": table.min_max_filtering(args, max=False)
		case "--max": table.min_max_filtering(args, max=True)
		case "--random": table.select_random_rows(10, preserve_order=True)
		case "--randomx": table.select_random_rows(10, preserve_order=False)

		case "--head": table.rows = table.rows[:10]
		case "--tail": table.rows = table.rows[-10:]
		case "--middle":
			start = (table.row_count - 10) // 2
			end = start + 10
			table.rows = table.rows[start:end]

		case "--mirror": table.mirror_table()
		case "--shuffle": random.shuffle(table.rows)
		case "--snip": table.snip_table(first_arg)
		case "--transpose": table.transpose_table()

		case "-p" | "--print": table.print_table()

		case _:
			print(f"Unknown manipulator: {flag}")


def manipulate_document(hotdoc, flag):
	manipulator = flag.flag

	match manipulator:
		case "--longest":
			hotdoc.tables = hotdoc.longest_tables()
		case "--widest":
			hotdoc.tables = hotdoc.widest_tables()
		case "--join":
			hotdoc.join_tables()
		case "--union":
			hotdoc.union_tables()
		case _:
			for table in hotdoc.tables:
				manipulate_table(table, flag)

def start_repl(hotdoc):
	while True:
		current_input = input("Hot >>> ").strip()
		if current_input in ["q", "quit", "exit"]:
			break
		elif not current_input:
			hotdoc.print_tables()
			continue
		elif current_input.isnumeric():
			n = int(current_input)
			hotdoc.print_tables(n)
			continue

		start_time = time.perf_counter()
		parts = current_input.split(" ")
		main, *rest = [part.strip() for part in parts]
		if len(main) == 1:
			main = f"-{main}"
		elif main[0] != "-":
			main = f"--{main}"

		flag = HotFlag(main)
		for arg in rest:
			flag.add_arg(arg)

		manipulate_document(hotdoc, flag)
		end_time = time.perf_counter()
		hotdoc.print_tables()

		execution_time = end_time - start_time
		formatted_time = format_duration_ns(execution_time * 1000_000_000)
		print(f"Execution finished in {formatted_time} seconds")

