


def pop_first_parenthesis_value(arg, default=None):
	start = arg.find('(')
	end = arg.find(')', start)

	if start != -1 and end != -1:
		value = arg[start+1:end]
		modified_string = arg[:start] + arg[end+1:]
		modified_string = modified_string.strip()
		return modified_string, value

	return arg, default # No parentheses found


