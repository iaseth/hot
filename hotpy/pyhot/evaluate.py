import re



alphabet = "abcdefghijklmnopqrstuvwxyz"

def transform(template, arr):
	for ch, val in zip(alphabet, arr):
		if ch in template:
			template = template.replace(ch, str(val))
	return template

def evaluate_template(template: str, arr: list):
	# Replace all $n occurrences with corresponding values
	transformed = transform(template, arr)
	try:
		return eval(transformed)
	except Exception as e:
		print(f"Error evaluating expression '{transformed}': {e}")

