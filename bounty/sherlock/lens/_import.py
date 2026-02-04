import ast

class FrappeImport:
	def __init__(self, node: ast.stmt):
		self.node = node
		self.line_number = node.lineno
		self.import_statement = ast.unparse(node)
		self.id = self.get_id()
		self.name = self.get_name()

	def get_id(self):
		if isinstance(self.node, ast.Import):
			return ",".join([alias.name for alias in self.node.names])
		elif isinstance(self.node, ast.ImportFrom):
			module = self.node.module if self.node.module else ""
			names = ",".join([alias.name for alias in self.node.names])
			return f"{module}:{names}"
		return ""

	def get_name(self):
		if isinstance(self.node, ast.Import):
			return ",".join([alias.name for alias in self.node.names])
		elif isinstance(self.node, ast.ImportFrom):
			return self.node.module if self.node.module else ""
		return ""

	def to_json(self):
		return {
			"id": self.id,
			"name": self.name,
			"import_statement": self.import_statement,
		}

def get_imports(body: list[ast.stmt]):
	imports = []
	for node in body:
		if isinstance(node, (ast.Import, ast.ImportFrom)):
			imports.append(FrappeImport(node))
	return imports
