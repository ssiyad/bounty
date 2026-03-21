import frappe
import frappe.utils
from frappe.query_builder.functions import Count


@frappe.whitelist()
def unread_count():
	Notification = frappe.qb.DocType("FS Notification")
	return (
		frappe.qb.from_(Notification)
		.where(Notification.hunter == frappe.session.user)
		.where(Notification.is_read == False)
		.select(Count(Notification.name).as_("count"))
		.run(as_dict=True)
		.pop()
		.get("count")
	)


@frappe.whitelist()
def mark_read():
	Notification = frappe.qb.DocType("FS Notification")
	return bool(
		frappe.qb.update(Notification)
		.where(Notification.hunter == frappe.session.user)
		.where(Notification.creation < frappe.utils.now_datetime())
		.where(Notification.is_read == False)
		.set(Notification.is_read, True)
		.run()
	)
