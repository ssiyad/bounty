import frappe
from frappe import _
from frappe.query_builder.builder import Order
from frappe.utils.caching import redis_cache
from pypika import Not


@frappe.whitelist(allow_guest=True)
def get_advisories(target: str | None = None, severity: str | None = None, my_reports: bool = False):
	Advisory = frappe.qb.DocType("Bounty Advisory")
	Report = frappe.qb.DocType("Bounty Report")
	return (
		frappe.qb.from_(Advisory)
		.left_join(Report)
		.on(Report.name == Advisory.report)
		.where(Advisory.published == 1)
		.where((Advisory.target == target) if target else Not(Advisory.target.isnull()))
		.where((Advisory.severity == severity) if severity else Not(Advisory.severity.isnull()))
		.where(Report.owner == frappe.session.user if my_reports else Not(Advisory.name.isnull()))
		.select(
			Advisory.name,
			Advisory.title,
			Advisory.severity,
			Advisory.target,
			Advisory.frappe_reference,
			Advisory.modified.as_("published_on"),
			Report.owner.as_("reported_by"),
		)
		.orderby(Advisory.modified, order=Order.desc)
		.run(as_dict=True)
	)


@frappe.whitelist(allow_guest=True)
@redis_cache()
def get_advisory(name: str):
	Advisory = frappe.qb.DocType("Bounty Advisory")
	Report = frappe.qb.DocType("Bounty Report")
	advisories = (
		frappe.qb.from_(Advisory)
		.left_join(Report)
		.on(Report.name == Advisory.report)
		.where(Advisory.published == 1)
		.where(Advisory.name == name)
		.select(
			Advisory.name,
			Advisory.title,
			Advisory.content,
			Advisory.severity,
			Advisory.target,
			Advisory.frappe_reference,
			Advisory.github_reference,
			Advisory.cve,
			Advisory.modified.as_("published_on"),
			Report.owner.as_("reported_by"),
		)
		.limit(1)
		.orderby(Advisory.modified, order=Order.desc)
		.run(as_dict=True)
	)
	if not advisories:
		message = _("Advisory with name {0} not found").format(name)
		frappe.throw(message, frappe.DoesNotExistError)
	return advisories[0]
