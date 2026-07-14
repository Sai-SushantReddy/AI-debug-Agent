from typing import TypedDict,Any

from langgraph.graph import StateGraph, START, END

from app.agents.error_analyzer import analyze_error
from app.agents.fix_generator import generate_fix
from app.agents.critic_agent import review_fix

from app.tools.syntax_checker import check_python_syntax
from app.tools.dependency_checker import check_dependencies

class DebugState(TypedDict):
    code: str
    error: str
    language: str

    error_analysis: str
    tool_result: dict[str, Any]
    proposed_fix: str
    validation_result: str
    final_report: dict

    retry_count: int



def analyze_error_node(state: DebugState):

    print("[1] ANALYZING ERROR")

    result = analyze_error(
        code=state["code"],
        error=state["error"],
        language=state["language"]
    )

    return {
        "error_analysis": result.model_dump()
    }

def select_tool_node(
    state: DebugState
) -> dict[str, Any]:

    print("[2] SELECTING DEBUG TOOL")

    error_type = state["error_analysis"][
        "error_type"
    ]

    if (
        state["language"].lower() == "python"
        and error_type == "SyntaxError"
    ):
        return {
            "tool_result": {
                "tool": "syntax_checker",
                "result": check_python_syntax(
                    state["code"]
                )
            }
        }

    if error_type in {
        "ImportError",
        "ModuleNotFoundError"
    }:
        return {
            "tool_result": {
                "tool": "dependency_checker",
                "result": check_dependencies(
                    state["code"]
                )
            }
        }

    return {
        "tool_result": {
            "tool": None,
            "result": {
                "message": (
                    "No deterministic tool "
                    "selected for this error type."
                )
            }
        }
    }

def generate_fix_node(state: DebugState):

    print("[2] GENERATING FIX")

    result = generate_fix(
        code=state["code"],
        error=state["error"],
        language=state["language"],
        error_analysis=str(
            state["error_analysis"]
        ),
        tool_result=str(
            state["tool_result"]
        )
    )

    return {
        "proposed_fix": result.model_dump()
    }


def validate_fix_node(
    state: DebugState
) -> dict[str, Any]:

    print("[4] VALIDATING FIX")

    fixed_code = state["proposed_fix"][
        "fixed_code"
    ]

    language = state["language"].lower()

    if language == "python":

        result = check_python_syntax(
            fixed_code
        )

        return {
            "validation_result": result
        }

    return {
        "validation_result": {
            "valid": False,
            "message": (
                f"Validation is not implemented "
                f"for {language}"
            )
        }
    }

def review_fix_node(state: DebugState):

    print("[4] REVIEWING FIX")

    fix = state["proposed_fix"]

    result = review_fix(
        original_code=state["code"],
        error=state["error"],
        fixed_code=fix["fixed_code"],
        explanation=fix["explanation"]
    )

    return {
        "final_report": {
            "error_analysis": state["error_analysis"],
            "tool_execution": state["tool_result"],
            "proposed_fix": state["proposed_fix"],
            "validation": state["validation_result"],
            "critic": result.model_dump()
        }
    }

graph = StateGraph(DebugState)

graph.add_node(
    "analyze_error",
    analyze_error_node
)

graph.add_node(
    "select_tool",
    select_tool_node
)

graph.add_node(
    "generate_fix",
    generate_fix_node
)

graph.add_node(
    "validate_fix",
    validate_fix_node
)

graph.add_node(
    "review_fix",
    review_fix_node
)

graph.add_edge(
    START,
    "analyze_error"
)

graph.add_edge(
    "analyze_error",
    "select_tool"
)

graph.add_edge(
    "select_tool",
    "generate_fix"
)

graph.add_edge(
    "generate_fix",
    "validate_fix"
)

graph.add_edge(
    "validate_fix",
    "review_fix"
)

graph.add_edge(
    "review_fix",
    END
)
debug_graph = graph.compile()