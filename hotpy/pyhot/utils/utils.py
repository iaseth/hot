


def format_duration_ns(ns):
	# Convert nanoseconds to seconds (1 second = 1_000_000_000 ns)
	seconds = ns / 1_000_000_000
	# Format with 9 digits after the decimal point
	formatted = f"{seconds:.9f}"
	# Split into integer and fractional parts
	int_part, frac_part = formatted.split(".")
	# Group fractional part in 3-digit segments
	grouped_frac = ".".join([frac_part[i:i+3] for i in range(0, 9, 3)])
	return f"{int_part}.{grouped_frac}"


