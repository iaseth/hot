import re



alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet_upper = alphabet.upper()

def transform(template, arr):
	for ch, val in zip(alphabet, arr):
		if ch in template:
			template = template.replace(ch, str(val))

	for ch_upper, val in zip(alphabet_upper, reversed(arr)):
		if ch_upper in template:
			template = template.replace(ch_upper, str(val))
	return template

def evaluate_template(template: str, arr: list):
	# Replace all $n occurrences with corresponding values
	transformed = transform(template, arr)
	try:
		return eval(transformed)
	except Exception as e:
		print(f"Error evaluating expression '{transformed}': {e}")

