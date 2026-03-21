# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class FSNotification(Document):
	def before_validate(self):
		self.ensure_hunter()

	def ensure_hunter(self):
		self.hunter = self.hunter or frappe.session.user

	def validate(self):
		self.validate_reference_doc()

	def validate_reference_doc(self):
		allowed_doctypes = ["FS Report"]
		if self.reference_doctype not in allowed_doctypes:
			message = _("Reference Doctype is not allowed")
			frappe.throw(message, frappe.ValidationError)


def permission_query(user=None):
	user = user or frappe.session.user
	return "(`tabFS Notification`.hunter = {0})".format(frappe.db.escape(user))


def has_permission(doc, ptype=None, user=None):
	if doc.is_new():
		return True
	user = user or frappe.session.user
	return doc.hunter == user
