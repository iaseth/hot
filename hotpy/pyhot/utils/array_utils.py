


def move_element_within_array(arr, m, n):
	if m < 0 or m >= len(arr):
		raise IndexError("Index m is out of range.")
	if n < 0 or n > len(arr):
		raise IndexError("Index n is out of range.")

	elem = arr.pop(m)
	arr.insert(n, elem)
	return arr


