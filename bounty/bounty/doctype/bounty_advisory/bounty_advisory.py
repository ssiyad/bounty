# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe
import frappe.utils
from frappe import _
from frappe.model.document import Document
from github import Auth, Github, GithubException


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

	@frappe.whitelist()
	def publish_to_github(self):
		"""Create and publish a security advisory on GitHub."""
		if not frappe.has_permission("Bounty Advisory", ptype="write", doc=self.name):
			message = _("Insufficient permissions to publish advisory.")
			frappe.throw(message, frappe.PermissionError)

		if self.github_reference:
			message = _("Advisory already published to GitHub: {0}").format(self.github_reference)
			frappe.throw(message, frappe.DuplicateEntryError)

		token = frappe.db.get_single_value("Bounty Settings", "github_token")
		if not token:
			message = _("GitHub token is not configured in Bounty Settings.")
			frappe.throw(message, frappe.PermissionError)

		repository = frappe.db.get_value("Bounty Target", self.target, "repository")
		if not repository:
			frappe.throw(_("Repository is not set on the Bounty Target {0}.").format(self.target))

		g = None
		try:
			g = Github(auth=Auth.Token(token))
			repo = g.get_repo(repository)
			advisory = repo.create_repository_advisory(
				summary=self.title,
				description=self.content,
				severity_or_cvss_vector_string=self.get_github_severity(self.severity),
				cve_id=self.cve,
			)
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

	def get_github_severity(self, severity: str):
		match severity:
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
