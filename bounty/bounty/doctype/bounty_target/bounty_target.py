# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import enum
import os
import pathlib
import re
import shutil

import frappe
import frappe.utils
import git
from frappe.model.document import Document

from bounty.bounty.doctype.sentinel_job.sentinel_job import schedule_job
from bounty.sherlock.doctype.sherlock_git_commit.sherlock_git_commit import SherlockGitCommit
from bounty.sherlock.doctype.sherlock_python_module.sherlock_python_module import SherlockPythonModule


class BountyTarget(Document):
	@property
	def backend_extensions(self):
		return ["py"]

	@property
	def frontend_extensions(self):
		return ["vue", "js", "ts"]

	@property
	def base_path(self):
		return pathlib.Path(frappe.utils.get_bench_path()).joinpath("sentinel").joinpath("sources").as_posix()

	@property
	def source_path(self):
		return pathlib.Path(self.base_path).joinpath(self.name).as_posix()

	@property
	def source_repo(self):
		return git.Repo(self.source_path)

	@property
	def last_commit(self):
		return self.source_repo.git.log(
			"-1",
			"--pretty=format:%H",
			"--branches",
			"develop",
		)

	@frappe.whitelist()
	def sync_code(self):
		frappe.enqueue_doc(self.doctype, self.name, "_sync_code", queue="long", now=True)

	def _sync_code(self):
		self.clean_up()
		git.Repo.clone_from(self.repository, self.source_path)

	@frappe.whitelist()
	def index_logs(self):
		frappe.enqueue_doc(self.doctype, self.name, "_index_logs", queue="long", now=True)

	def _index_logs(self):
		for commit in self.source_repo.iter_commits("develop"):
			SherlockGitCommit.from_object(self.source_repo, self.name, commit)
			frappe.db.commit()

	@frappe.whitelist()
	def index_code(self):
		frappe.enqueue_doc(self.doctype, self.name, "_index_code", queue="long", now=True)

	def _index_code(self):
		base_path = pathlib.Path(self.source_path).joinpath(self.backend_source)
		for root, _, files in os.walk(base_path):
			for file in files:
				if file.split(".").pop() not in self.backend_extensions:
					continue
				p = str(pathlib.Path(root).joinpath(file).relative_to(self.source_path))
				d = "Sherlock Python Module"
				if frappe.db.exists(
					{
						"doctype": d,
						"revision": self.last_commit,
						"source": self.name,
						"path": p,
					}
				):
					continue
				m: SherlockPythonModule = frappe.new_doc(d)
				m.path = p
				m.revision = self.last_commit
				m.source = self.name
				m.save()
				m.index_classes()
		self._index_endpoint_usages()

	def _index_endpoint_usages(self):
		extensions = ("vue", "js", "ts")
		pattern = re.compile(r"url: [\'|\"](.*)[\'|\"]")
		for source in self.frontend_sources:
			for root, _, files in os.walk(pathlib.Path(self.source_path).joinpath(source.directory)):
				for file in files:
					if file.split(".")[-1] not in extensions:
						continue
					with open(os.path.join(root, file)) as source_code:
						for line_number, line in enumerate(source_code):
							if match := pattern.search(line):
								method = match.group(1).removeprefix("/api/method/")
								if frappe.db.exists(
									{
										"doctype": "Sherlock Endpoint",
										"identifier": method,
										"source": self.name,
										"revision": self.last_commit,
									}
								):
									continue
								usage = frappe.new_doc("Sherlock Endpoint Usage")
								usage.file = str(
									pathlib.Path(root).joinpath(file).relative_to(self.source_path)
								)
								usage.line_number = line_number
								usage.identifier = method
								usage.source_id = self.name
								usage.revision = self.last_commit
								usage.insert()

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
