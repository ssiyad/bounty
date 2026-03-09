import frappe
from frappe.query_builder.builder import Order
from pypika import Not


@frappe.whitelist()
def get_advisories(target: str | None = None, severity: str | None = None):
	Advisory = frappe.qb.DocType("Bounty Advisory")
	CondTarget = Advisory.target == target if target else Not(Advisory.target.isnull())
	CondSeverity = Advisory.severity == severity if severity else Not(Advisory.severity.isnull())
	return (
		frappe.qb.from_(Advisory)
		.where(Advisory.published == 1)
		.where(CondTarget)
		.where(CondSeverity)
		.select(
			Advisory.name,
			Advisory.title,
			Advisory.severity,
			Advisory.target,
			Advisory.frappe_reference,
			Advisory.modified.as_("published_on"),
		)
		.orderby(Advisory.modified, order=Order.desc)
		.run(as_dict=True)
	)
