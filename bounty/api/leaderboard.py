import frappe
import frappe.utils
from frappe.query_builder import Order
from frappe.query_builder.functions import Count


@frappe.whitelist()
def get_leaderboard():
	"""
	Returns the leaderboard data with minimal information for each user. Limited to last 30 days
	and top 10 users.
	"""
	Report = frappe.qb.DocType("Bounty Report")
	Hunter = frappe.qb.DocType("Bounty Hunter")
	User = frappe.qb.DocType("User")
	return (
		frappe.qb.from_(Report)
		.inner_join(Hunter)
		.on(Report.hunter == Hunter.name)
		.inner_join(User)
		.on(Hunter.user == User.name)
		.where(Report.creation >= frappe.utils.add_to_date(frappe.utils.now(), days=-30))
		.where(Report.status == "Accepted")
		.groupby(Hunter.name)
		.select(User.full_name.as_("name"), Count(Report.name).as_("score"))
		.orderby(Count(Report.name), order=Order.desc)
		.limit(10)
		.run(as_dict=True)
	)
