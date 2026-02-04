import ast


def get_doc_with_input(args: list[str], body: list[ast.stmt]):
	occurances = []
	for node in ast.walk(ast.Module(body=body)):
		if isinstance(node, ast.Call):
			if isinstance(node.func, ast.Attribute):
				if node.func.attr == "get_doc":
					if len(node.args) >= 2:
						second_arg = node.args[1]
						if isinstance(second_arg, ast.Name):
							if second_arg.id in args:
								occurances.append({
									"arg": second_arg.id,
									"lineno": node.lineno,
								})
	return occurances
