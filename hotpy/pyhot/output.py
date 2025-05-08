import xml.etree.ElementTree as ET

from jinja2 import Environment, PackageLoader, select_autoescape



env = Environment(
	loader=PackageLoader("pyhot"),
	autoescape=select_autoescape()
)
env.trim_blocks = True
env.lstrip_blocks = True
table_template = env.get_template("table.html")


def document_to_html5(document):
	html = table_template.render(document=document)
	return html


def document_to_html(document):
	root = ET.Element('section')
	for table in document.tables:
		table_tag = ET.SubElement(root, 'table')
		thead = ET.SubElement(table_tag, 'thead')
		tr = ET.SubElement(thead, 'tr')
		for header in table.headers:
			child = ET.SubElement(tr, "th")
			child.text = str(header)

		tbody = ET.SubElement(table_tag, 'tbody')
		for i, row in enumerate(table.rows, start=1):
			tr = ET.SubElement(tbody, 'tr')
			for value in [i, *row]:
				child = ET.SubElement(tr, "td")
				child.text = str(value)

	tree = ET.ElementTree(root)
	ET.indent(tree, space=document.space, level=0)
	html_string = ET.tostring(root, encoding='unicode')
	return html_string


def document_to_xml(document):
	root = ET.Element('data')

	for table in document.tables:
		table_tag = ET.SubElement(root, 'HotTable')
		for row in table.rows:
			row_tag = ET.SubElement(table_tag, 'HotRow')
			for header, value in zip(table.headers, row):
				child = ET.SubElement(row_tag, header)
				child.text = str(value)

	tree = ET.ElementTree(root)
	ET.indent(tree, space=document.space, level=0)
	# tree.write('output.xml', encoding='unicode')
	xml_string = ET.tostring(root, encoding='unicode')
	return xml_string

