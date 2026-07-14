from typing import Any


def check_python_syntax(
    code: str
) -> dict[str, Any]:

    try:
        compile(
            code,
            "<debug-agent>",
            "exec"
        )

        return {
            "valid": True,
            "error_type": None,
            "message": None,
            "line": None,
            "offset": None
        }

    except SyntaxError as error:
        return {
            "valid": False,
            "error_type": type(error).__name__,
            "message": error.msg,
            "line": error.lineno,
            "offset": error.offset
        }