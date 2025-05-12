import readline
import time
import os
import atexit

from .colorprint import printc, color
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
	hash_1 = hotdoc.hash

	while True:
		try:
			current_input = input(color("Hot >>> ", "bright_yellow")).strip()
			if current_input in ["q", "quit", "exit"]:
				break
			elif current_input in ["qq"]:
				hotdoc.save_document()
				break
			elif not current_input:
				hotdoc.print_tables()
				continue
			elif current_input.isnumeric():
				n = int(current_input)
				hotdoc.print_tables(n)
				continue

			parts = current_input.split(" ")
			main, *rest = [part.strip() for part in parts]
			if len(main) == 1:
				main = f"-{main}"
			elif main[0] != "-":
				main = f"--{main}"

			flag = HotFlag(main)
			for arg in rest:
				flag.add_arg(arg)

			start_time = time.perf_counter()
			manipulate_document(hotdoc, flag)
			end_time = time.perf_counter()
			hash_2 = hotdoc.hash

			if hash_2 == hash_1:
				print(f"Nothing happened!")
			else:
				hotdoc.print_tables()
				hash_1 = hash_2

			execution_time = end_time - start_time
			formatted_time = format_duration_ns(execution_time * 1000_000_000)
			printc(f"Execution finished in {formatted_time} seconds", "bright_green")
		except (EOFError, KeyboardInterrupt):
			print("\nGoodbye!")
			break

