


def camelize(s):
	parts = [p.capitalize() for p in s.split()]
	camel = "".join(parts)
	camel = camel[0].lower() + camel[1:]
	return camel


