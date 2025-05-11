


def pop_first_value_between_xny(arg, start_char='(', end_char=')', default=None):
	start = arg.find(start_char)
	end = arg.find(end_char, start)

	if start != -1 and end != -1:
		value = arg[start+1:end]
		modified_string = arg[:start] + arg[end+1:]
		modified_string = modified_string.strip()
		return modified_string, value

	return arg, default # No parentheses found


