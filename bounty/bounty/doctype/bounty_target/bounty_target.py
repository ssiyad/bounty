# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import pathlib
import shutil

import frappe
import frappe.utils
import git
from frappe.model.document import Document

from bounty.bounty.doctype.sentinel_job.sentinel_job import schedule_job


class BountyTarget(Document):
	@property
	def base_path(self):
		return pathlib.Path(frappe.utils.get_bench_path()).joinpath("sentinel").joinpath("sources").as_posix()

	@property
	def source_path(self):
		return pathlib.Path(self.base_path).joinpath(self.name).as_posix()

	@property
	def source_repo(self):
		return git.Repo(self.source_path)

	@frappe.whitelist()
	def sync_code(self):
		schedule_job("Sync Code", self.doctype, self.name, "_get_code")

	def _sync_code(self):
		self.clean_up()
		git.Repo.clone_from(self.repository, self.source_path)

	def clean_up(self):
		shutil.rmtree(self.source_path, ignore_errors=True)

	def search_history(self, query: str):
		commit, user = None, None
		result = self.source_repo.git.log(
			"-1",
			"--pretty=format:%H\n%an",
			"-S",
			query,
			"--branches",
			"develop",
		).split("\n")
		if len(result) == 2:
			commit, user = result
		return {
			"last_commit": commit,
			"last_user": user,
		}
