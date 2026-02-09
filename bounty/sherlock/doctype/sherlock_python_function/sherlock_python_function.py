# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import ast

import frappe
from frappe.model.document import Document
from frappe.query_builder import Order


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
		d.line_number = node.lineno
		d.arguments = ", ".join(arg.arg for arg in node.args.args)
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
		self.set_guest_access()
		self.set_last_seen_commit()

	def set_whitelisted(self):
		decorators = ["frappe.whitelist()", "frappe.whitelist(allow_guest=True)"]
		self.whitelisted = any(x.decorator_name in decorators for x in self.decorators)

	def set_guest_access(self):
		self.guest_access = any("allow_guest=True" in x.decorator_name for x in self.decorators)

	def set_last_seen_commit(self):
		Commit = frappe.qb.DocType("Sherlock Git Commit")
		commit = (
			frappe.qb.from_(Commit)
			.select(Commit.revision)
			.select(Commit.author_name)
			.where(Commit.source == self.source)
			.where(Commit.diff.like(f"%{self.identifier}%"))
			.orderby(Commit.date, order=Order.desc)
			.limit(1)
			.run(as_dict=True)
		)
		if commit:
			self.last_seen_commit = commit[0].revision
			self.last_author = commit[0].author_name
		else:
			self.last_seen_commit = None
			self.last_author = None
