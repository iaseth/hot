


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



def to_int(s):
	if s == "-": return 0
	if s[-1] == "*":
		s = s[:-1]

	try:
		return int(s)
	except ValueError:
		return 0


