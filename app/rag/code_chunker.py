import ast

from app.workflows.state import (
    RepositoryFileState,
    RetrievedContextState
)


def chunk_python_file(
    file: RepositoryFileState
) -> list[RetrievedContextState]:

    code = file["content"]

    try:
        tree = ast.parse(code)

    except SyntaxError:
        return [
            {
                "path": file["path"],
                "symbol": "<module>",
                "chunk_type": "module",
                "content": code
            }
        ]

    chunks: list[RetrievedContextState] = []

    for node in ast.walk(tree):

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
                ast.ClassDef
            )
        ):
            source = ast.get_source_segment(
                code,
                node
            )

            if source is None:
                continue

            chunks.append(
                {
                    "path": file["path"],
                    "symbol": node.name,
                    "chunk_type": (
                        "class"
                        if isinstance(node, ast.ClassDef)
                        else "function"
                    ),
                    "content": source
                }
            )

    if not chunks:
        chunks.append(
            {
                "path": file["path"],
                "symbol": "<module>",
                "chunk_type": "module",
                "content": code
            }
        )

    return chunks

def chunk_repository(
    files: list[RepositoryFileState]
) -> list[RetrievedContextState]:

    chunks: list[RetrievedContextState] = []

    for file in files:

        if file["path"].endswith(".py"):
            chunks.extend(
                chunk_python_file(file)
            )

        else:
            chunks.append(
                {
                    "path": file["path"],
                    "symbol": "<module>",
                    "chunk_type": "module",
                    "content": file["content"]
                }
            )

    return chunks