# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe
import frappe.utils
from frappe import _
from frappe.model.document import Document


class BountyAdvisory(Document):
	def before_validate(self):
		self.ensure_frappe_reference()

	def ensure_frappe_reference(self):
		self.frappe_reference = self.frappe_reference or self.generate_frappe_reference()

	def generate_frappe_reference(self):
		prefix = "FSA"
		year = frappe.utils.now_datetime().year
		return "{}-{}-{}".format(prefix, year, str(self.name).upper())

	def validate(self):
		self.validate_target()

	def validate_target(self):
		if self.report:
			target = frappe.get_value("Bounty Report", self.report, "target")
			if target != self.target:
				message = _("Target does not match the target in the report.")
				frappe.throw(message)
