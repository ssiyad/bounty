# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class BountyAttempt(Document):
	pass


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
