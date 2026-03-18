import frappe
from frappe import _


@frappe.whitelist()
def get_draft(name: str):
	d = frappe.get_doc("Bounty Draft", name)
	if d.hunter != frappe.session.user:
		message = _("You do not have access to this draft.")
		frappe.throw(message, frappe.PermissionError)
	return {
		"name": d.name,
		"title": d.title,
		"content": d.content,
	}


@frappe.whitelist()
def create_draft(name: str, title: str, content: str):
	d = frappe.new_doc("Bounty Draft")
	d.hunter = frappe.session.user
	d.title = title
	d.content = content
	d.save()
	return d.name


@frappe.whitelist()
def save_draft(name: str, title: str, content: str):
	if not title:
		message = _("Title is required.")
		frappe.throw(message, frappe.ValidationError)
	if not content:
		message = _("Content is required.")
		frappe.throw(message, frappe.ValidationError)
	d = frappe.get_doc("Bounty Draft", name)
	if d.hunter != frappe.session.user:
		message = _("You do not have access to this draft.")
		frappe.throw(message, frappe.PermissionError)
	d.title = title
	d.content = content
	d.save()
