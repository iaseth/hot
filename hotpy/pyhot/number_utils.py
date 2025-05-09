


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



def to_int(val):
	if val == "-": return 0
	if "." in val:
		val = val.split(".")[0]
	if val[-1] == "*":
		val = val[:-1]

	try:
		return int(val)
	except ValueError:
		return 0

def to_float(val):
	if val == "-": return 0.0

	try:
		return float(val)
	except ValueError:
		return 0


