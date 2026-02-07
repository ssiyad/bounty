import ast

from ._import import get_imports
from ._decorator import get_decorators
from .patterns.get_doc import get_doc_with_input

class FrappeFunction:
	def __init__(self, path: str, parent: str, node: ast.FunctionDef):
		self.node = node
		self.id = parent + '.' + node.name
		self.name = node.name
		self.path = path
		self.parent = parent
		self.line_number = node.lineno
		self.args = [arg.arg for arg in node.args.args]
		self.decorator_list = get_decorators(node)
		self.imports = get_imports(node.body)
		self.get_doc_with_input = get_doc_with_input(self.args, self.node.body)

	def to_json(self):
		return {
			"id": self.id,
			"name": self.name,
			"path": self.path,
			"parent": self.parent,
			"line_number": self.line_number,
			"args": self.args,
			"decorators": [x.to_json() for x in self.decorator_list],
			"imports": [x.to_json() for x in self.imports],
			"get_doc_with_input": self.get_doc_with_input,
		}

def get_functions(path: str, parent: str, body: list[ast.stmt]) -> list[FrappeFunction]:
	functions = []
	for node in body:
		if isinstance(node, ast.FunctionDef):
			functions.append(FrappeFunction(path, parent, node))
	return functions
