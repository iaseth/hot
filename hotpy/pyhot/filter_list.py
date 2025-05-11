from .utils import is_int



def filter_list(arr, s):
	if s is None:
		return arr
	elif is_int(s):
		index = int(s)
		return arr[:index]
	elif "," in s:
		parts = [p for p in s.split(",") if p and is_int(p)]
		indices = [int(p) for p in parts]
		arr = [arr[i] for i in indices]
		return arr

	try:
		# Parse slice string
		parts = s.split(':')
		if len(parts) > 3:
			raise ValueError("Invalid slice format")
		slice_args = [int(p) if p else None for p in parts]
		return arr[slice(*slice_args)]
	except Exception as e:
		raise ValueError(f"Invalid filter string: {s}") from e


def filter_list_by_args(arr, args):
	for arg in args:
		arr = filter_list(arr, arg)
	return arr

