import frappe


def create_notification(hunter: str, doctype: str, docname: str, *content: str):
	d = frappe.new_doc("FS Notification")
	d.hunter = hunter
	d.reference_doctype = doctype
	d.reference_docname = docname
	d.content = " ".join(content)
	return d.insert(ignore_permissions=True)


def create_reference_anchor(doctype: str, docname: str):
	"""Create a url that can be used to refer other pages in frontend."""
	protocol = "frappe-security"
	path = "reference-doc"
	doctype_prefix = "FS "
	doctype = doctype.lstrip(doctype_prefix)
	text = doctype.lower()
	return f"{protocol}:{path}:doctype={doctype}&docname={docname}&text={text}"
