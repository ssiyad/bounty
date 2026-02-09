# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import ast
import pathlib

import frappe
import frappe.utils
from frappe.model.document import Document

from bounty.sherlock.doctype.sherlock_python_function.sherlock_python_function import SherlockPythonFunction


class SherlockPythonModule(Document):
	@property
	def source_doc(self):
		return frappe.get_doc("Bounty Target", self.source)

	@property
	def source_code(self):
		try:
			with open(
				pathlib.Path(frappe.utils.get_bench_path())
				.joinpath(self.source_doc.source_path)
				.joinpath(self.path)
			) as f:
				return f.read()
		except:
			return ""

	@property
	def walkable_tree(self):
		return ast.walk(ast.parse(self.source_code))

	def before_validate(self):
		self.identifier = self.path.removesuffix(".py").replace("/", ".")
		self.module_name = self.identifier

	def after_insert(self):
		self.index_functions()

	def index_functions(self):
		for node in self.walkable_tree:
			if not isinstance(node, ast.FunctionDef):
				continue
			SherlockPythonFunction.from_node(
				source=self.source_doc.name,
				revision=self.source_doc.last_commit,
				module_id=self.name,
				class_id=None,
				parent_identifier=self.identifier,
				path=self.path,
				node=node,
			)
		frappe.db.commit()

	def index_classes(self):
		for node in self.walkable_tree:
			if not isinstance(node, ast.ClassDef):
				continue
			d = "Sherlock Python Class"
			if frappe.db.exists(
				{
					"doctype": d,
					"revision": self.source_doc.last_commit,
					"source": self.source_doc.name,
					"path": self.path,
				}
			):
				continue
			c = frappe.new_doc(d)
			c.source = self.source_doc.name
			c.revision = self.source_doc.last_commit
			c.module = self.name
			c.path = self.path
			c.class_name = node.name
			c.save()
