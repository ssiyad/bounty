# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe
import frappe.utils
from frappe import _
from frappe.core.doctype.communication.communication import Communication
from frappe.model.document import Document

from security.utils.notification import create_notification, create_reference_anchor


class FSReport(Document):
	def before_validate(self):
		self.ensure_hunter()

	def ensure_hunter(self):
		if self.is_new():
			self.hunter = frappe.session.user

	def on_update(self):
		self.notify_status_change()

	def notify_status_change(self):
		if self.has_value_changed("status") and self.status != "Pending":
			anchor = create_reference_anchor(self.doctype, self.name)
			content = ("Your", anchor, "has been", self.status.lower())
			create_notification(self.hunter, self.doctype, self.name, *content)

	@frappe.whitelist()
	def reply(self, content: str):
		from_user = str(frappe.session.user)
		user = frappe.get_doc("User", from_user)
		doc: Communication = frappe.new_doc("Communication")
		doc.subject = self.get_title()
		doc.content = content
		doc.status = "Linked"
		doc.sent_or_received = "Received" if self.owner == frappe.session.user else "Sent"
		doc.communication_type = "Communication"
		doc.communication_date = frappe.utils.now_datetime()
		doc.communication_medium = "Chat"
		doc.reference_doctype = self.doctype
		doc.reference_name = self.name
		doc.sender_full_name = user.full_name
		doc.user = from_user
		doc.insert(ignore_permissions=True)
		self.notify_reply()

	def notify_reply(self):
		if self.hunter == frappe.session.user:
			return
		anchor = create_reference_anchor(self.doctype, self.name)
		content = ("There is a new message on your", anchor)
		create_notification(self.hunter, self.doctype, self.name, *content)


def permission_query(user: str | None = None):
	user = user or frappe.session.user
	return "(`tabFS Report`.hunter = {0}".format(frappe.db.escape(user))


def has_permission(doc, ptype=None, user=None):
	if doc.is_new():
		return True
	user = user or frappe.session.user
	return doc.hunter == user
