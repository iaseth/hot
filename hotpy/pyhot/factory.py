from .table import HotTable
from .filter_list import filter_list
from .utils import is_int, is_float



def get_row_cols(tr, cols_filter):
	cells = tr.find_all("th")
	if not cells:
		cells = tr.find_all("td")
	data = [cell.text.strip() for cell in cells]
	data = filter_list(data, cols_filter)
	return data


def create_table_from_table_tag(table_tag, args):
	thead = table_tag.find("thead")
	tbody = table_tag.find("tbody")

	if thead and tbody:
		headers = get_row_cols(thead.find('tr'), args.c1)
		tr_tags = tbody.find_all("tr")
	else:
		tr_tags = table_tag.find_all("tr")
		headers = get_row_cols(tr_tags[0], args.c1)
		tr_tags = tr_tags[1:]

	tr_tags = filter_list(tr_tags, args.r1)
	rows = [get_row_cols(tr, args.c1) for tr in tr_tags]

	n_cols = len(rows[0])
	rows_are_uniform = all(len(row) == n_cols for row in rows)
	if rows_are_uniform:
		for n in range(n_cols):
			all_values_are_int = all(is_int(row[n]) for row in rows)
			all_values_are_float = all(is_float(row[n]) for row in rows)
			if all_values_are_int:
				for row in rows:
					row[n] = int(row[n])
			elif all_values_are_float:
				for row in rows:
					row[n] = float(row[n])

	hot_table = HotTable()
	hot_table.headers = headers
	hot_table.rows = rows
	return hot_table

