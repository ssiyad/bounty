# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class SherlockPythonModule(Document):
	def before_validate(self):
		self.identifier = self.path.removesuffix(".py").replace("/", ".")
		self.module_name = self.identifier
