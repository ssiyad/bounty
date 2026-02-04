import ast
import os
import re
import frappe

from bounty.sherlock.lens._function import FrappeFunction

from ._module import FrappeModule

@frappe.whitelist()
def modules():
	path = "/home/ssiyad/sources/cloud/apps/press/press/api/"
	modules = []
	for root, _, files in os.walk(path):
		for file in files:
			if not file.endswith(".py"):
				continue
			modules.append(FrappeModule(path, root, file))
	return [module.to_json() for module in modules]


@frappe.whitelist()
def functions():
	path = "/home/ssiyad/sources/cloud/apps/press/press/api/"
	functions = []
	for root, _, files in os.walk(path):
		for file in files:
			if not file.endswith(".py"):
				continue
			module = FrappeModule(path, root, file)
			functions.extend(module.functions)
	return [function.to_json() for function in functions]


@frappe.whitelist()
def endpoints():
	path = "/home/ssiyad/sources/cloud/apps/press/"
	functions: list[FrappeFunction] = []
	for root, _, files in os.walk(path):
		for file in files:
			if not file.endswith(".py"):
				continue
			module = FrappeModule(path, root, file)
			functions.extend(module.functions)
	endpoints: list[FrappeFunction] = []
	for function in functions:
		if (any(c.isupper() for c in function.id)):
			continue
		if not (any(d.name == 'frappe.whitelist' for d in function.decorator_list)):
			continue
		endpoints.append(function)
	return endpoints


@frappe.whitelist()
def used_endpoints() -> list[str]:
	dashboard_path = "/home/ssiyad/sources/cloud/apps/press/dashboard/"
	extensions = ['vue', 'js', 'ts']
	pattern = re.compile(r'url: [\'|\"](.*)[\'|\"]')
	used_endpoints = set()
	for root, _, files in os.walk(dashboard_path):
		for file in files:
			if not file.split('.')[-1] in extensions:
				continue
			with open(os.path.join(root, file), "r") as source_code:
				for line in source_code:
					if match := pattern.search(line):
						method = match.group(1).removeprefix('/api/method/')
						used_endpoints.add(method)
	return list(used_endpoints)


@frappe.whitelist()
def unused_endpoints():
	all_endpoints = endpoints()
	all_used_endpoints = used_endpoints()
	unused_endpoints: list[FrappeFunction] = []
	print(all_used_endpoints)
	for endpoint in all_endpoints:
		if endpoint.id not in all_used_endpoints:
			unused_endpoints.append(endpoint)
	return [endpoint.to_json() for endpoint in unused_endpoints]
