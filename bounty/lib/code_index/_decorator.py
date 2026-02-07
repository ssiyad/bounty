import ast


class FrappeDecorator:
	def __init__(self, node: ast.expr):
		self.node = node
		self.name = self.get_name()
		self.args = self.get_args()
		self.kwargs = self.get_kwargs()

	def get_name(self) -> str:
		if isinstance(self.node, ast.Call):
			return ast.unparse(self.node.func)
		return ast.unparse(self.node)

	def get_args(self) -> list[str]:
		args = []
		if isinstance(self.node, ast.Call):
			for arg in self.node.args:
				args.append(ast.unparse(arg))
		return args

	def get_kwargs(self) -> dict[str, str]:
		kwargs = {}
		if isinstance(self.node, ast.Call):
			for keyword in self.node.keywords:
				kwargs[keyword.arg] = ast.unparse(keyword.value)
		return kwargs

	def to_json(self):
		return {
			"name": self.name,
			"args": self.args,
			"kwargs": self.kwargs,
		}


def get_decorators(node: ast.FunctionDef) -> list[FrappeDecorator]:
	decorators = []
	for decorator in node.decorator_list:
		decorators.append(FrappeDecorator(decorator))
	return decorators
