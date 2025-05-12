# colorprint.py

# ANSI color codes
COLORS = {
	"black": "\033[30m",
	"red": "\033[31m",
	"green": "\033[32m",
	"yellow": "\033[33m",
	"blue": "\033[34m",
	"magenta": "\033[35m",
	"cyan": "\033[36m",
	"white": "\033[37m",
	"bright_black": "\033[90m",
	"bright_red": "\033[91m",
	"bright_green": "\033[92m",
	"bright_yellow": "\033[93m",
	"bright_blue": "\033[94m",
	"bright_magenta": "\033[95m",
	"bright_cyan": "\033[96m",
	"bright_white": "\033[97m",
	"reset": "\033[0m"
}

def color(text: str, color_name: str) -> str:
	code = COLORS.get(color_name.lower())
	if code is None:
		raise ValueError(f"Unknown color: {color_name}")
	return f"{code}{text}{COLORS['reset']}"

def print_colored(text: str, color: str, end: str="\n") -> None:
	"""
	Prints the text in the specified color.
	:param text: The text to print
	:param color: The color name (e.g., "red", "bright_blue")
	"""
	code = COLORS.get(color.lower())
	if code is None:
		raise ValueError(f"Unknown color: {color}")
	print(f"{code}{text}{COLORS['reset']}", end=end)

def print_all_colors(text: str = "Sample Text") -> None:
	"""
	Prints the text in all available colors.
	"""
	for color in COLORS:
		if color == "reset":
			continue
		print_colored(f"{color:<15}: {text}", color)

printc = print_colored

if __name__ == "__main__":
	print_all_colors()
