# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe
import frappe.utils
from frappe import _
from frappe.core.doctype.communication.communication import Communication
from frappe.model.document import Document
from frappe.query_builder import Order


class BountyReport(Document):
	def before_validate(self):
		self.ensure_hunter()

	def ensure_hunter(self):
		self.hunter = frappe.session.user

	@frappe.whitelist()
	def chat(self):
		Chat = frappe.qb.DocType("Communication")
		return (
			frappe.qb.from_(Chat)
			.select(Chat.name.as_("id"))
			.select(Chat.content)
			.select(Chat.communication_date.as_("date"))
			.select(Chat.sent_or_received)
			.where(Chat.reference_doctype == self.doctype)
			.where(Chat.reference_name == self.name)
			.orderby(Chat.communication_date, order=Order.desc)
			.run(as_dict=True)
		)

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
		return self.chat()


def permission_query(user: str | None = None):
	user = user or frappe.session.user
	return "(`tabBounty Attempt`.hunter = {0})".format(frappe.db.escape(user))


def has_permission(doc: BountyHunter, ptype="read", user: str | None = None):
	user = user or frappe.session.user
	return doc.hunter == user
