from typing import Any


def search_code(
    project_files: list[dict[str, str]],
    query: str
) -> dict[str, Any]:

    matches: list[dict[str, Any]] = []

    normalized_query = query.lower()

    for file in project_files:

        path = file["path"]
        content = file["content"]

        for line_number, line in enumerate(
            content.splitlines(),
            start=1
        ):

            if normalized_query in line.lower():

                matches.append(
                    {
                        "path": path,
                        "line": line_number,
                        "content": line.strip()
                    }
                )

    return {
        "query": query,
        "matches": matches,
        "match_count": len(matches)
    }