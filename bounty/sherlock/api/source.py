import frappe
from frappe.query_builder.functions import Count
from frappe.utils.caching import redis_cache
from frappe.utils.typing_validations import validate_argument_types


@frappe.whitelist()
@validate_argument_types
def overview(source: str):
	frappe.only_for("Bounty Manager")
	source_doc = frappe.get_doc("Bounty Target", source)
	return {
		"commit_count": commit_count(source),
		"function_count": functions_count(source, source_doc.last_commit),
		"endpoint_count": endpoints_count(source, source_doc.last_commit),
	}


@redis_cache()
def commit_count(source: str):
	Source = frappe.qb.DocType("Bounty Target")
	GitCommit = frappe.qb.DocType("Sherlock Git Commit")
	return (
		(
			frappe.qb.from_(Source)
			.left_join(GitCommit)
			.on(Source.name == GitCommit.source)
			.select(Count(GitCommit.name).as_("count"))
			.where(Source.name == source)
		)
		.run(as_dict=True)
		.pop()
		.get("count", 0)
	)


@redis_cache()
def functions_count(source: str, commit: str):
	Source = frappe.qb.DocType("Bounty Target")
	PythonFunction = frappe.qb.DocType("Sherlock Python Function")
	return (
		frappe.qb.from_(PythonFunction)
		.left_join(Source)
		.on(Source.name == PythonFunction.source)
		.select(Count(PythonFunction.name).as_("count"))
		.where(Source.name == source)
		.where(PythonFunction.revision == commit)
		.run(as_dict=True)
		.pop()
		.get("count", 0)
	)


@redis_cache()
def endpoints_count(source: str, commit: str):
	Source = frappe.qb.DocType("Bounty Target")
	PythonFunction = frappe.qb.DocType("Sherlock Python Function")
	PythonFunctionDecorator = frappe.qb.DocType("Sherlock Python Function Decorator")
	return (
		frappe.qb.from_(PythonFunctionDecorator)
		.left_join(PythonFunction)
		.on(PythonFunction.name == PythonFunctionDecorator.parent)
		.left_join(Source)
		.on(Source.name == PythonFunction.source)
		.select(Count(PythonFunctionDecorator.name).as_("count"))
		.where(Source.name == source)
		.where(PythonFunction.revision == commit)
		.where(PythonFunctionDecorator.decorator_name.like("frappe.whitelist%"))
		.run(as_dict=True)
		.pop()
		.get("count", 0)
	)
