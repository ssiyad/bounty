# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import ast

import frappe
from frappe.model.document import Document


class SherlockPythonFunction(Document):
	@staticmethod
	def from_node(
		source: str,
		revision: str,
		module_id: str,
		class_id: str | None,
		parent_identifier: str,
		path: str,
		node: ast.FunctionDef,
	):
		identifier = parent_identifier + "." + node.name
		doctype = "Sherlock Python Function"
		if frappe.db.exists(
			{
				"doctype": doctype,
				"source": source,
				"revision": revision,
				"identifier": identifier,
			}
		):
			return
		d = frappe.new_doc(doctype)
		d.source = source
		d.revision = revision
		d.module_id = module_id
		d.class_id = class_id
		d.identifier = identifier
		d.function_name = node.name
		d.path = path
		for decorator in node.decorator_list:
			if isinstance(decorator, ast.Name):
				d.append(
					"decorators",
					{
						"decorator_name": decorator.id,
						"arguments": None,
					},
				)
			elif isinstance(decorator, ast.Attribute):
				parts = []
				current = decorator
				while isinstance(current, ast.Attribute):
					parts.append(current.attr)
					current = current.value
				if isinstance(current, ast.Name):
					parts.append(current.id)
				d.append(
					"decorators",
					{
						"decorator_name": ".".join(reversed(parts)),
						"arguments": None,
					},
				)
			else:
				d.append(
					"decorators",
					{
						"decorator_name": ast.unparse(decorator),
						"arguments": None,
					},
				)
		return d.save()

	def before_validate(self):
		self.set_whitelisted()

	def set_whitelisted(self):
		decorators = ["frappe.whitelist()", "frappe.whitelist(allow_guest=True)"]
		self.whitelisted = any(x.decorator_name in decorators for x in self.decorators)
