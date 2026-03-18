import frappe
from frappe import _


@frappe.whitelist(methods=["POST"])
def create_report(title: str, content: str):
	report = frappe.new_doc("Bounty Report")
	report.hunter = frappe.session.user
	report.title = title
	report.content = content
	report = report.insert(ignore_permissions=True)
	return report.name


@frappe.whitelist()
def get_reports():
	Report = frappe.qb.DocType("Bounty Report")
	return (
		frappe.qb.from_(Report)
		.select(
			Report.name,
			Report.title,
			Report.content,
			Report.status,
			Report.target,
			Report.category,
			Report.severity,
			Report.creation,
		)
		.where(Report.hunter == frappe.session.user)
		.run(as_dict=True)
	)


@frappe.whitelist()
def get_report(name: str):
	Report = frappe.qb.DocType("Bounty Report")
	report = (
		frappe.qb.from_(Report)
		.select(
			Report.name,
			Report.title,
			Report.content,
			Report.status,
			Report.target,
			Report.category,
			Report.severity,
		)
		.where(Report.name == name)
		.where(Report.hunter == frappe.session.user)
		.run(as_dict=True)
	)
	if not report:
		message = _("Report not found")
		frappe.throw(message, frappe.DoesNotExistError)
	return report[0]
