# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

from collections.abc import Callable

import frappe
import frappe.utils
from frappe.model.document import Document


class SentinelJob(Document):
	pass


def m_(doctype: str, docname: str, method_name: str, sentinel_id: str, **kwargs):
	doc = frappe.get_doc(doctype, docname)
	job = frappe.get_doc("Sentinel Job", sentinel_id)
	try:
		getattr(doc, method_name)(**kwargs)
		job.status = "Success"
	except:
		job.status = "Failure"
	finally:
		job.finished_on = frappe.utils.now_datetime()
		job.save()


def schedule_job(title: str, doctype: str, docname: str, method: str, **kwargs):
	job = frappe.new_doc("Sentinel Job")
	job.title = title
	job.reference_doctype = doctype
	job.reference_docname = docname
	job.started_on = frappe.utils.now_datetime()
	job = job.save()
	return frappe.enqueue(
		method=m_,
		doctype=doctype,
		docname=docname,
		method_name=method,
		sentinel_id=job.name,
		**kwargs,
	)
