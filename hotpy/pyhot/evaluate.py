import re



def replace_match(match, arr):
	index = int(match.group(1))
	if 0 <= index < len(arr):
		return str(arr[index])
	return "0"

def evaluate_template(template: str, arr: list):
	# Replace all $n occurrences with corresponding values
	replaced = re.sub(r'\@(\d+)', lambda x:replace_match(x, arr), template)
	try:
		return eval(replaced)
	except Exception as e:
		print(f"Error evaluating expression '{replaced}': {e}")

