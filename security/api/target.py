import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def get_targets():
	Target = frappe.qb.DocType("FS Target")
	return (
		frappe.qb.from_(Target)
		.select(Target.name, Target.title, Target.logo, Target.repository)
		.run(as_dict=True)
	)


@frappe.whitelist(allow_guest=True)
def get_target(name: str):
	Target = frappe.qb.DocType("FS Target")
	target = (
		frappe.qb.from_(Target)
		.where(Target.name == name)
		.select(Target.name, Target.title, Target.logo, Target.repository)
		.run(as_dict=True)
	)
	if not target:
		message = _("Target {0} not found").format(name)
		frappe.throw(message, frappe.DoesNotExistError)
	return target[0]
