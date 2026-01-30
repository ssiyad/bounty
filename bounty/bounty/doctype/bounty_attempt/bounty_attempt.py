# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import Order
import frappe.utils
from frappe import _
from frappe.model.document import Document
from frappe.core.doctype.communication.communication import Communication


class BountyAttempt(Document):
	@frappe.whitelist()
	def chat(self):
		Chat = frappe.qb.DocType("Communication")
		return (
			frappe.qb.from_(Chat)
			.select(Chat.name)
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
		from_user = frappe.session.user
		hunter = hunter_id(from_user)
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
		doc.sender_full_name = frappe.db.get_value("Bounty Hunter", hunter, "display_name")
		doc.user = from_user
		doc.insert(ignore_permissions=True)
		return self.chat()


def permission_query(user_id: str | None=None):
	user_id = user_id or frappe.session.user
	return "(`tabBounty Attempt`.hunter = {0})".format(frappe.db.escape(hunter_id(user_id)))


def has_permission(doc: BountyHunter, ptype="read", user:str | None=None):
	user_id = user or frappe.session.user
	return doc.hunter == hunter_id(user_id)


def hunter_id(user_id: str):
	id = frappe.db.get_value("Bounty Hunter", {"user_id": user_id})
	if not id:
		message = _("Bounty Hunter profile not found.")
		frappe.throw(message, frappe.ValidationError)
	return id
