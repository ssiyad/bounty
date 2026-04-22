# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import urllib.parse

import frappe
import frappe.utils
from frappe import _
from frappe.model.document import Document
from github import Auth, Github, GithubException

from security.utils.notification import create_notification, create_reference_anchor


class FSAdvisory(Document):
	def before_validate(self):
		self.ensure_frappe_reference()

	def ensure_frappe_reference(self):
		self.frappe_reference = self.frappe_reference or self.generate_frappe_reference()

	def generate_frappe_reference(self):
		prefix = "FSA"
		year = frappe.utils.now_datetime().year
		return "{}-{}-{}".format(prefix, year, str(self.name).upper())

	def validate(self):
		self.validate_report()
		self.validate_target()

	def validate_report(self):
		if not self._report:
			return
		if self._report.status != "Accepted":
			message = _("Report must be accepted to create an advisory.")
			frappe.throw(message)

	def validate_target(self):
		if self.report:
			target = frappe.get_value("FS Report", self.report, "target")
			if target != self.target:
				message = _("Target does not match the target in the report.")
				frappe.throw(message)

	def on_update(self):
		self.notify_publish()

	def notify_publish(self):
		if self.has_value_changed("published") and self.published and self._report:
			anchor_advisory = create_reference_anchor(self.doctype, self.name)
			anchor_report = create_reference_anchor(self._report.doctype, self._report.name)
			content = ("An", anchor_advisory, "has been published against your", anchor_report)
			create_notification(self._report.hunter, self._report.doctype, self._report.name, *content)

	@frappe.whitelist()
	def publish_to_github(self):
		if not frappe.has_permission("FS Advisory", ptype="write", doc=self.name):
			message = _("Insufficient permissions to publish advisory.")
			frappe.throw(message, frappe.PermissionError)

		if self.github_reference:
			message = _("Advisory already published to GitHub: {0}").format(self.github_reference)
			frappe.throw(message, frappe.DuplicateEntryError)

		token = frappe.db.get_single_value("FS Settings", "github_token")
		if not token:
			message = _("GitHub token is not configured in Security Settings.")
			frappe.throw(message, frappe.PermissionError)

		repository = self._target.repository
		if not repository:
			message = _("Repository is not set on the Target {0}.").format(self.target)
			frappe.throw(message)
		repository = urllib.parse.urlparse(repository).path.strip("/")

		g = None
		try:
			g = Github(auth=Auth.Token(token))
			repo = g.get_repo(repository)
			advisory = repo.create_repository_advisory(
				summary=self.title,
				description=self.content,
				severity_or_cvss_vector_string=self.get_github_severity(),
				cve_id=self.cve,
				vulnerabilities=self.get_vulenerablities(),
			)
			advisory.publish()
			advisory.request_cve()
			self.github_reference = advisory.ghsa_id
			self.published = 1
			self.save()
			message = _("Advisory published to GitHub: <a href='{0}' target='_blank'>{1}</a>").format(
				advisory.html_url, advisory.ghsa_id
			)
			frappe.msgprint(message, title=_("Success"), indicator="green")
		except GithubException as e:
			message = _("GitHub API error: {0}").format(str(e))
			frappe.throw(message)
		finally:
			if g:
				g.close()

	def get_github_severity(self):
		match self.severity:
			case "Informational":
				return "low"
			case "Low":
				return "low"
			case "Medium":
				return "medium"
			case "High":
				return "high"
			case "Critical":
				return "critical"
			case _:
				return "low"

	def get_vulenerablities(self):
		return [
			{
				"package": {
					"ecosystem": "other",
					"name": self._target.title,
				},
				"vulnerable_version_range": "<" + version,
				"patched_versions": version,
				"vulnerable_functions": [],
			}
			for version in self.get_patched_versions()
		]

	def get_patched_versions(self) -> list[str]:
		return [v.strip() for v in self.patched_version.split(",")]

	@property
	def _target(self):
		return frappe.get_doc("FS Target", self.target)

	@property
	def _report(self):
		return frappe.get_doc("FS Report", self.report) if self.report else None
