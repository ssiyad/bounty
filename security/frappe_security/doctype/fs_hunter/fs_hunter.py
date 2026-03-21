# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class FSHunter(Document):
	pass


def permission_query(user: str | None = None):
	user = user or frappe.session.user
	return "(`tabFS Hunter`.user = {0})".format(frappe.db.escape(user))


def has_permission(doc: FSHunter, ptype="read", user: str | None = None):
	user = user or frappe.session.user
	return doc.user == user


def create_hunter(doc, method=None):
	"""To be used from hooks after inserting a new user."""
	try:
		doc.add_roles("Security Hunter")
		hunter = frappe.new_doc("FS Hunter")
		hunter.user = doc.name
		doc.save()
		return hunter.insert(ignore_permissions=True)
	except:
		frappe.db.rollback()
		message = _("Failed to create Hunter for user {0}").format(doc.name)
		frappe.throw(message, frappe.MandatoryError)
