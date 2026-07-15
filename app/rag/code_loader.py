from app.workflows.state import RepositoryFileState


SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cpp",
    ".c"
}

IGNORED_DIRECTORIES = {
    "node_modules",
    "venv",
    ".venv",
    ".git",
    "__pycache__"
}


def filter_repository_files(
    project_files: list[RepositoryFileState]
) -> list[RepositoryFileState]:

    filtered_files: list[RepositoryFileState] = []

    for file in project_files:
        path = file["path"]

        path_parts = path.split("/")

        if any(
            directory in IGNORED_DIRECTORIES
            for directory in path_parts
        ):
            continue

        if not any(
            path.endswith(extension)
            for extension in SUPPORTED_EXTENSIONS
        ):
            continue

        filtered_files.append(file)

    return filtered_files