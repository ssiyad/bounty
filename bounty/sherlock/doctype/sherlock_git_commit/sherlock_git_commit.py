# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe
import frappe.utils
from frappe.model.document import Document
from git import Commit


class SherlockGitCommit(Document):
	@staticmethod
	def from_object(source: str, commit: Commit):
		doctype = "Sherlock Git Commit"
		if frappe.db.exists(
			{
				"doctype": doctype,
				"source": source,
				"revision": commit.hexsha,
			}
		):
			return
		d = frappe.new_doc(doctype)
		d.source = source
		d.date = frappe.utils.get_date_str(commit.committed_datetime)
		d.revision = commit.hexsha
		d.message = commit.message
		d.author_name = commit.author.name
		d.author_email = commit.author.email
		d.diff = "".join(d.diff.decode("utf-8") for d in commit.diff(create_patch=True))
		return d.save()
