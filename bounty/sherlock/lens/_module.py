import ast
import pathlib

from ._class import get_classes
from ._function import get_functions
from ._import import get_imports

class FrappeModule:
	def __init__(self, base_path: str, root: str, file: str):
		self.root = root
		self.file = file
		self.path = pathlib.Path(root).joinpath(file)
		self.path_relative = str(self.path.relative_to(base_path))
		self.id = self.path_relative.removesuffix(".py").replace("/", ".")
		self.name = self.id.split(".")[-1]
		self.tree = self.get_tree()
		self.imports = get_imports(self.tree.body)
		self.classes = get_classes(self.path_relative, self.id, self.tree.body)
		self.functions = get_functions(self.path_relative, self.id, self.tree.body)

	def get_tree(self):
		with open(self.path, "r") as f:
			return ast.parse(f.read())

	def to_json(self):
		return {
			"root": self.root,
			"file": self.file,
			"path": str(self.path),
			"path_relative": self.path_relative,
			"id": self.id,
			"name": self.name,
			"imports": [x.to_json() for x in self.imports],
			"classes": [x.to_json() for x in self.classes],
			"functions": [x.to_json() for x in self.functions],
		}
