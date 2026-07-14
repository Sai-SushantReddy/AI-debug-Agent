import ast
import importlib.util
from typing import Any


def extract_imports(code: str) -> list[str]:

    try:
        tree = ast.parse(code)

    except SyntaxError:
        return []

    imports: set[str] = set()

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for alias in node.names:
                imports.add(
                    alias.name.split(".")[0]
                )

        elif isinstance(node, ast.ImportFrom):

            if node.module:
                imports.add(
                    node.module.split(".")[0]
                )

    return list(imports)


def check_dependencies(
    code: str
) -> dict[str, Any]:

    imports = extract_imports(code)

    missing_dependencies: list[str] = []

    for package in imports:

        try:
            package_spec = importlib.util.find_spec(
                package
            )

        except (
            ImportError,
            ModuleNotFoundError,
            ValueError
        ):
            package_spec = None

        if package_spec is None:
            missing_dependencies.append(package)

    return {
        "imports": imports,
        "missing_dependencies": missing_dependencies,
        "valid": len(missing_dependencies) == 0
    }