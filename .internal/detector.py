import ast
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent

for python_file in project_dir.glob("*.py"):  # Directly in the parent folder
    try:
        tree = ast.parse(python_file.read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as error:
        print(f"{python_file.name}: could not parse ({error})")
        continue

    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add("." * node.level + node.module)

    print(f"{python_file.name}: {sorted(modules)}")