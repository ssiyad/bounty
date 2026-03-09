import frappe
from frappe.query_builder.builder import Order
from pypika import Not


@frappe.whitelist()
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
		.where(Report.owner == frappe.session.user if my_reports else Not(Report.owner.isnull()))
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
