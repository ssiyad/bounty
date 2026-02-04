import os
import pathlib
import re

import frappe
from frappe.utils import caching

from bounty.sherlock.lens._function import FrappeFunction

from ._module import FrappeModule


def functions(target: str):
	target = frappe.get_doc("Bounty Target", "Cloud")
	functions: list[FrappeFunction] = []
	for root, _, files in os.walk(target.source_path):
		for file in files:
			if not file.endswith(".py"):
				continue
			module = FrappeModule(target.source_path, root, file)
			functions.extend(module.functions)
	return functions


def endpoints(target: str):
	all_functions = functions(target)
	endpoints: list[FrappeFunction] = []
	for function in all_functions:
		if any(c.isupper() for c in function.id):
			continue
		if not (any(d.name == "frappe.whitelist" for d in function.decorator_list)):
			continue
		endpoints.append(function)
	return endpoints


def used_endpoints(target: str) -> list[str]:
	target = frappe.get_doc("Bounty Target", target)
	extensions = ["vue", "js", "ts"]
	pattern = re.compile(r"url: [\'|\"](.*)[\'|\"]")
	used_endpoints = set()
	for frontend_source in target.frontend_sources:
		for root, _, files in os.walk(pathlib.Path(target.source_path).joinpath(frontend_source.directory)):
			for file in files:
				if file.split(".")[-1] not in extensions:
					continue
				with open(os.path.join(root, file)) as source_code:
					for line in source_code:
						if match := pattern.search(line):
							method = match.group(1).removeprefix("/api/method/")
							used_endpoints.add(method)
	return list(used_endpoints)


@frappe.whitelist()
@caching.redis_cache(ttl=60 * 60)
def unused_endpoints(target: str):
	target_doc = frappe.get_doc("Bounty Target", target)
	all_endpoints = endpoints(target)
	all_used_endpoints = used_endpoints(target)
	unused_endpoints: list[FrappeFunction] = []
	for endpoint in all_endpoints:
		if endpoint.id not in all_used_endpoints:
			unused_endpoints.append(endpoint)
	unused_endpoints_ = []
	for endpoint in unused_endpoints:
		unused_endpoints_.append(
			{
				**endpoint.to_json(),
				**target_doc.search_history(endpoint.id),
			}
		)
	return unused_endpoints_
