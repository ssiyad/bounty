# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe
import frappe.utils
from frappe import _
from frappe.core.doctype.communication.communication import Communication
from frappe.model.document import Document


class BountyReport(Document):
	def before_validate(self):
		self.ensure_hunter()

	def ensure_hunter(self):
		self.hunter = frappe.session.user

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

	@frappe.whitelist()
	def create_advisory(self):
		if not self.target:
			msg = _("Target is required to create an advisory.")
			frappe.throw(msg)
		if self.status != "Accepted":
			msg = _("Report must be accepted to create an advisory.")
			frappe.throw(msg)
		doctype = "Bounty Advisory"
		doc = frappe.new_doc(doctype)
		doc.report = self.name
		doc.target = self.target
		doc.title = self.title
		doc.content = self.content
		doc.published = False
		doc = doc.insert()
		url = frappe.utils.get_url_to_form(doctype, doc.name)
		msg = "Bounty Advisory <a href='{0}'>{1}</a> created successfully.".format(url, doc.name)
		frappe.msgprint(msg)
