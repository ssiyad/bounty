# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FSDraft(Document):
	def before_validate(self):
		self.ensure_hunter()

	def ensure_hunter(self):
		self.hunter = frappe.session.user

	def on_submit(self):
		self.create_report()

	def create_report(self):
		"""Create a report from this draft."""
		report = frappe.new_doc("FS Report")
		report.hunter = self.hunter
		report.target = self.target if self.target else None
		report.severity = self.severity if self.severity else None
		report.title = self.title
		report.content = self.content
		report = report.save()
		self.move_attachments(report.name)

	def move_attachments(self, docname: str):
		File = frappe.qb.DocType("File")
		return bool(
			frappe.qb.update(File)
			.set(File.attached_to_doctype, "FS Report")
			.set(File.attached_to_name, docname)
			.where(File.attached_to_doctype == self.doctype)
			.where(File.attached_to_name == self.name)
			.run()
		)

	@frappe.whitelist()
	def submit_draft(self):
		"""Proxy to `self.submit`."""
		return self.submit()


def permission_query(user: str | None = None):
	user = user or frappe.session.user
	return "(`tabFS Draft`.hunter = {0} AND `tabFS Draft`.docstatus = 0)".format(frappe.db.escape(user))


def has_permission(doc, ptype=None, user=None):
	if doc.is_new():
		return True
	user = user or frappe.session.user
	return doc.hunter == user
