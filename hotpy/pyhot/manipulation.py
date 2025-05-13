import uuid

from .utils import filter_list_by_args, strip_leading_dots
from .utils import to_bool, to_int, to_float, to_str, to_rounded



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
		case "--drop-naked": table.drop_naked_columns()
		case "--keep": table.keep_certain_columns(column_indexes)
		case "--move": flag.forEachArg(table.move_column)
		case "--swap": flag.forEachArg(table.swap_two_columns)

		# undocumented
		case "--parens": flag.forEachArg(table.extract_column_between_parens)
		case "--braces": flag.forEachArg(table.extract_column_between_braces)
		case "--brackets": flag.forEachArg(table.extract_column_between_brackets)

		case "--min": table.min_max_filtering(args, max=False)
		case "--max": table.min_max_filtering(args, max=True)
		case "--random": table.select_random_rows(10, preserve_order=True)
		case "--randomx": table.select_random_rows(10, preserve_order=False)

		case "--first-word": table.choose_nth_word(args, n=0)
		case "--last-word": table.choose_nth_word(args, n=-1)
		case "--nth-word": table.choose_nth_word(args)
		case "--slice": table.slice_column(args)

		case "--head": table.rows = table.rows[:flag.get_first_int(default=10)]
		case "--tail": table.rows = table.rows[-flag.get_first_int(default=10):]
		case "--middle":
			n = flag.get_first_int(default=10)
			start = (table.row_count - n) // 2
			end = start + n
			table.rows = table.rows[start:end]

		case "--left": table.choose_n_columns_from_left(flag.get_first_int())
		case "--right": table.choose_n_columns_from_left(flag.get_first_int(), right=True)

		case "--mirror": table.mirror_table()
		case "--shuffle": random.shuffle(table.rows)
		case "--snip": table.snip_table(first_arg)
		case "--transpose": table.transpose_table()

		case "-p" | "--print": table.print_table()
		case "--gh" | "--github": table.print_table(fmt="github")

		case _:
			print(f"Unknown manipulator: {flag}")


def manipulate_document(hotdoc, flag):
	manipulator = flag.flag

	match manipulator:
		case "--longest":
			hotdoc.tables = hotdoc.longest_tables()
		case "--widest":
			hotdoc.tables = hotdoc.widest_tables()
		case "--join": hotdoc.join_tables()
		case "--union": hotdoc.union_tables()

		case "--empty": hotdoc.empty_document()
		case "--load": hotdoc.load_document()
		case "--save": hotdoc.save_document()

		case "--snap": hotdoc.time_machine.snap()
		case "--forget": hotdoc.time_machine.forget()
		case "--history": hotdoc.time_machine.history()
		case "--undo": hotdoc.time_machine.undo()
		case "--redo": hotdoc.time_machine.redo()
		case _:
			for table in hotdoc.tables:
				manipulate_table(table, flag)

