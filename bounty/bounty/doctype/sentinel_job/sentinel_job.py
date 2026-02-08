# Copyright (c) 2026, Sabu Siyad and contributors
# For license information, please see license.txt

import traceback

import frappe
import frappe.utils
from frappe.model.document import Document


class SentinelJob(Document):
	pass


def m_(doctype: str, docname: str, method_name: str, sentinel_id: str, **kwargs):
	doc = frappe.get_doc(doctype, docname)
	job = frappe.get_doc("Sentinel Job", sentinel_id)
	try:
		job.output = str(getattr(doc, method_name)(**kwargs))
		job.status = "Success"
	except Exception as e:
		tb = traceback.format_exc()
		frappe.log_error(
			title=e,
			message=tb,
			reference_doctype=doctype,
			reference_name=docname,
		)
		job.error = str(e)
		job.traceback = tb
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
		enqueue_after_commit=True,
		**kwargs,
	)
