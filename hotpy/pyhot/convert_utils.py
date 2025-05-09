


def to_bool(val):
	if val in ["-", "", 0, 0.0]:
		return False
	return True if val else False


def to_int(val):
	if val == "-": return 0
	if val[-1] in ["%", "*"]:
		val = val[:-1]
	if "." in val:
		val = val.split(".")[0]
	if "," in val:
		val = "".join(val.split(","))

	try:
		return int(val)
	except ValueError:
		return 0


def to_float(val):
	if val == "-": return 0.0
	if val[-1] in ["%"]:
		val = val[:-1]

	try:
		return float(val)
	except ValueError:
		return 0


def to_str(val):
	if isinstance(val, str):
		return val
	return str(val)


