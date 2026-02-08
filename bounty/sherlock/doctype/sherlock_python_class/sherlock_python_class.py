# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SherlockPythonClass(Document):
	@property
	def module_doc(self):
		return frappe.get_doc("Sherlock Python Module", self.module)

	def before_validate(self):
		self.identifier = self.module_doc.identifier + "." + self.class_name
