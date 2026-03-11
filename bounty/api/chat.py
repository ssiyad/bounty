import frappe
from frappe import _
from frappe.query_builder import Case, Order


@frappe.whitelist()
def get_messages(report: str):
	Report = frappe.qb.DocType("Bounty Report")
	Chat = frappe.qb.DocType("Communication")
	# Reverse the sent_or_received value to show messages from the perspective of the hunter.
	Direction = Case().when(Chat.sent_or_received == "Sent", "Received").else_("Sent").as_("sent_or_received")
	return (
		frappe.qb.from_(Chat)
		.inner_join(Report)
		.on(Chat.reference_name == Report.name)
		.where(Chat.reference_doctype == "Bounty Report")
		.where(Chat.reference_name == report)
		.where(Report.name == report)
		.where(Report.hunter == frappe.session.user)
		.select(Chat.name.as_("id"))
		.select(Chat.content)
		.select(Chat.communication_date.as_("date"))
		.select(Direction)
		.orderby(Chat.communication_date, order=Order.desc)
		.run(as_dict=True)
	)


@frappe.whitelist(methods=["POST"])
def send_message(report: str, content: str):
	report = frappe.get_doc("Bounty Report", report)
	user = frappe.get_doc("User", frappe.session.user)
	if report.hunter != user.name:
		message = _("You do not have access to this report.")
		frappe.throw(message, frappe.PermissionError)
	report.reply(content)
	return get_messages(report.name)
