import uuid



def manipulate_table(table, flag):
	manipulator = flag.flag

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
		case _:
			print(f"Unknown manipulator: '{manipulator}'")


