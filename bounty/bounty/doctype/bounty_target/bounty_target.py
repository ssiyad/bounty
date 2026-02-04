# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import os
import pathlib
import git

import frappe
import frappe.utils
from frappe.model.document import Document


class BountyTarget(Document):
	@property
	def base_path(self):
		return (
			pathlib.Path(frappe.utils.get_bench_path())
			.joinpath("sentinel")
			.joinpath("sources")
			.as_posix()
		)

	@property
	def source_path(self):
		return pathlib.Path(self.base_path).joinpath(self.name).as_posix()

	@frappe.whitelist()
	def	get_code(self):
		self.clean_up()
		git.Repo.clone_from(self.repository, self.source_path)

	def clean_up(self):
		if os.path.exists(self.source_path):
			os.rmdir(self.source_path)
