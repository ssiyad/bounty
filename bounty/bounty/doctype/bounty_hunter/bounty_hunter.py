# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe
import randomname
from frappe.core.doctype.user.user import User
from frappe.model.document import Document


class BountyHunter(Document):
	@property
	def user(self) -> User:
		return frappe.get_doc("User", self.user_id)

	def before_insert(self):
		self.ensure_username()
		self.ensure_display_name()

	def ensure_username(self):
		self.username = self.generate_username()

	def ensure_display_name(self):
		self.display_name = self.generate_display_name(self.username)

	def generate_username(self):
		is_duplicate = True
		username = randomname.get_name()
		while is_duplicate:
			username = randomname.get_name()
			is_duplicate = frappe.db.exists("Bounty Hunter", {"username": username})
		return username

	def generate_display_name(self, username: str):
		return username.replace("-", " ").title()

	def validate(self):
		self.prevent_duplicate()
		self.prevent_real_name()

	def prevent_duplicate(self):
		if not self.has_value_changed("user_id"):
			return
		exists = frappe.db.exists({"doctype": "Bounty Hunter", "user_id": self.user.name})
		if exists:
			frappe.throw(f"Bounty Hunter {self.user.full_name} already exists.")

	def prevent_real_name(self):
		if self.username == self.user.username:
			frappe.throw("Username must be different from real name.")


def permission_query(user_id: str | None = None):
	user_id = user_id or frappe.session.user
	return "(`tabBounty Hunter`.user_id = {0})".format(frappe.db.escape(user_id))


def has_permission(doc: BountyHunter, ptype="read", user: str | None = None):
	user_id = user or frappe.session.user
	return doc.user_id == user_id


def from_user(user: User, method: str | None = None) -> BountyHunter:
	return frappe.get_doc(
		{
			"doctype": "Bounty Hunter",
			"user_id": user.name,
			"username": frappe.mock("name"),
			"display_name": frappe.mock("name"),
		}
	).save()
