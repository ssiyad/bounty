import functools

import frappe


def skip_admin(fn):
	"""Skip function if the user is an admin."""

	@functools.wraps(fn)
	def inner(*args, **kwargs):
		if frappe.session.user == "Administrator":
			return True
		if "Security Manager" in frappe.get_roles(frappe.session.user):
			return True
		return fn(*args, **kwargs)

	return inner
