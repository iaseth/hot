


def is_int(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def is_float(s):
	try:
		float(s)
		return True
	except ValueError:
		return False


def filter_array(arr, s):
	if s is None:
		return arr
	elif is_int(s):
		index = int(s)
		return arr[:index]

	try:
		# Parse slice string
		parts = s.split(':')
		if len(parts) > 3:
			raise ValueError("Invalid slice format")
		slice_args = [int(p) if p else None for p in parts]
		return arr[slice(*slice_args)]
	except Exception as e:
		raise ValueError(f"Invalid filter string: {s}") from e

