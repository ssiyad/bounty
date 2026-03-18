# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BountyDraft(Document):
	def before_validate(self):
		self.ensure_hunter()

	def ensure_hunter(self):
		self.hunter = frappe.session.user

	def on_submit(self):
		self.create_report()

	def create_report(self):
		"""Create a report from this draft."""
		report = frappe.new_doc("Bounty Report")
		report.hunter = self.hunter
		report.title = self.title
		report.content = self.content
		report.save()

	@frappe.whitelist()
	def submit_draft(self):
		"""Proxy to `self.submit`."""
		return self.submit()


def permission_query(user: str | None = None):
	user = user or frappe.session.user
	return "(`tabBounty Draft`.hunter = {0} AND `tabBounty Draft`.docstatus = 0)".format(
		frappe.db.escape(user)
	)


def has_permission(doc, ptype=None, user=None):
	if doc.is_new():
		return True
	user = user or frappe.session.user
	return doc.hunter == user
