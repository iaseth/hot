from .evaluate import alphabet



def camelize(s):
	parts = [p.capitalize() for p in s.split()]
	camel = "".join(parts)

	if camel[0].isupper():
		camel = camel[0].lower() + camel[1:]
	elif camel[0].isnumeric():
		camel = "x" + camel

	return camel


def get_snippet_args(arg: str):
	parts = arg.lower().split(":")
	if len(parts) != 2:
		return None

	p1, p2 = parts
	if len(p1) < 2 or len(p1) < 2:
		return None
	elif not p1[0].isalpha() or not p2[0].isalpha():
		return None
	elif not p1[1:].isnumeric() or not p2[1:].isnumeric():
		return None

	c1 = alphabet.index(p1[0])
	c2 = alphabet.index(p2[0])
	r1 = int(p1[1:])
	r2 = int(p2[1:])

	if not c1 < c2: return None
	if not r1 < r2: return None
	if r1 <= 0 or r2 <= 0: return None

	return (c1, r1, c2, r2)


