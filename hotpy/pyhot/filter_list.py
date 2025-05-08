from .utils import is_int



def filter_list(arr, s):
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

