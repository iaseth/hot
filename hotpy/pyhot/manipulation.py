import uuid

from .convert_utils import to_bool, to_int, to_float, to_str
from .convert_utils import strip_leading_dots, to_rounded



def manipulate_table(table, flag):
	manipulator = flag.flag
	hotargs = flag.args
	args = flag.string_args

	match manipulator:
		case "--id":
			table.headers = ["Id", *table.headers]
			table.rows = [[i+1, *row] for i, row in enumerate(table.rows)]
		case "--index":
			table.headers = ["Index", *table.headers]
			table.rows = [[i, *row] for i, row in enumerate(table.rows)]
		case "--uuid":
			table.headers = ["UUID", *table.headers]
			table.rows = [[str(uuid.uuid4()), *row] for row in table.rows]

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

		case _:
			print(f"Unknown manipulator: '{manipulator}'")


