import re



alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet_upper = alphabet.upper()

def transform_template(template, arr):
	for ch, val in zip(alphabet, arr):
		if ch in template:
			template = template.replace(ch, str(val))

	for ch_upper, val in zip(alphabet_upper, reversed(arr)):
		if ch_upper in template:
			template = template.replace(ch_upper, str(val))
	return template

def evaluate_expression(expression: str, arr: list):
	try:
		return eval(expression)
	except Exception as e:
		print(f"Error evaluating expression '{expression}': {e}")
		return 0

def evaluate_template(template: str, arr: list):
	expression = transform_template(template, arr)
	return evaluate_expression(expression, arr)

