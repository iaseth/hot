


def camelize(s):
	parts = [p.capitalize() for p in s.split()]
	camel = "".join(parts)

	if camel[0].isupper():
		camel = camel[0].lower() + camel[1:]
	elif camel[0].isnumeric():
		camel = "x" + camel

	return camel


