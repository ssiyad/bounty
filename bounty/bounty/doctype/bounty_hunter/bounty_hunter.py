# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe
import randomname
from frappe.core.doctype.user.user import User
from frappe.model.document import Document


class BountyHunter(Document):
	pass


def permission_query(user_id: str | None = None):
	user_id = user_id or frappe.session.user
	return "(`tabBounty Hunter`.user_id = {0})".format(frappe.db.escape(user_id))


def has_permission(doc: BountyHunter, ptype="read", user: str | None = None):
	user = user or frappe.session.user
	return doc.user == user


def from_user(user: User, method: str | None = None) -> BountyHunter:
	user.add_roles("Bounty Hunter")
	hunter = frappe.new_doc("Bounty Hunter")
	hunter.user = user.name
	return hunter.insert(ignore_permissions=True)
