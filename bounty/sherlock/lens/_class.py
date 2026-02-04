import ast

from ._function import get_functions

class FrappeClass:
	def __init__(self, path:str, parent: str, node: ast.ClassDef):
		self.node = node
		self.name = node.name
		self.path = path
		self.parent = parent
		self.bases = [base.id for base in node.bases if isinstance(base, ast.Name)]
		self.methods = get_functions(self.path, self.name, self.node.body)

	def to_json(self):
		return {
			"path": self.path,
			"name": self.name,
			"parent": self.parent,
			"bases": self.bases,
			"methods": [method.to_json() for method in self.methods],
		}

def get_classes(path: str, parent: str, body: list[ast.stmt]):
	classes = []
	for node in body:
		if isinstance(node, ast.ClassDef):
			classes.append(FrappeClass(path, parent, node))
	return classes
