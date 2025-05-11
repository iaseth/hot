import readline
import time
import os
import atexit

from .hotparse import HotFlag
from .manipulation import manipulate_document
from .utils import format_duration_ns


HISTORY_FILE = os.path.expanduser("~/.hottable_repl_history")

def load_history():
	if os.path.exists(HISTORY_FILE):
		readline.read_history_file(HISTORY_FILE)

def save_history():
	readline.write_history_file(HISTORY_FILE)


def start_repl(hotdoc):
	load_history()
	atexit.register(save_history)

	while True:
		try:
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
		except (EOFError, KeyboardInterrupt):
			print("\nGoodbye!")
			break

