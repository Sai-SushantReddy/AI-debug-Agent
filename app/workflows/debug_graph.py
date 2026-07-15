from app.workflows.state import DebugState

from langgraph.graph import StateGraph, START, END

from app.agents.error_analyzer import analyze_error
from app.agents.fix_generator import generate_fix
from app.agents.critic_agent import review_fix

from app.tools.syntax_checker import check_python_syntax
from app.tools.dependency_checker import check_dependencies

from app.rag.code_loader import filter_repository_files
from app.rag.code_chunker import chunk_repository
from app.rag.vector_store import create_repository_collection
from app.rag.retriever import retrieve_context


def analyze_error_node(
    state: DebugState
) -> dict[str, object]:

    print("[1] ANALYZING ERROR")

    result = analyze_error(
        code=state["code"],
        error=state["error"],
        language=state["language"]
    )

    return {
        "error_analysis": result.model_dump()
    }

def retrieve_context_node(
    state: DebugState
) -> dict[str, object]:

    print("[2] RETRIEVING REPOSITORY CONTEXT")

    files = filter_repository_files(
        state["project_files"]
    )

    chunks = chunk_repository(files)

    if not chunks:
        return {
            "retrieved_context": []
        }

    collection = create_repository_collection(
        chunks
    )

    query = (
        f"{state['error']} "
        f"{state['error_analysis']['probable_cause']} "
        f"{state['code']}"
    )

    contexts = retrieve_context(
        collection=collection,
        query=query,
        top_k=min(3, len(chunks))
    )

    return {
        "retrieved_context": contexts
    }

def route_repository_context(
    state: DebugState
) -> str:

    requires_context = state[
        "error_analysis"
    ]["requires_repository_context"]

    has_project_files = bool(
        state["project_files"]
    )

    if requires_context and has_project_files:
        return "retrieve_context"

    return "select_tool"


def select_tool_node(
    state: DebugState
) -> dict[str, object]:

    print("[3] SELECTING DEBUG TOOL")

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

def generate_fix_node(
        state: DebugState
        ) -> dict[str,object]:

    print("[4] GENERATING FIX")

    result = generate_fix(
        code=state["code"],
        error=state["error"],
        language=state["language"],
        error_analysis=str(
            state["error_analysis"]
        ),
        tool_result=str(
            state["tool_result"]
        ),
        retrieved_context=str(
            state["retrieved_context"]
        )
    )

    return {
        "proposed_fix": result.model_dump()
    }

def validate_fix_node(
    state: DebugState
) -> dict[str, object]:

    print("[5] VALIDATING FIX")

    language = state["language"].lower()

    file_changes = state[
        "proposed_fix"
    ]["file_changes"]

    validation_results: list[dict[str, object]] = []

    for file_change in file_changes:

        path = file_change["path"]
        fixed_code = file_change["fixed_code"]

        if (
            language == "python"
            and path.endswith(".py")
        ):
            result = check_python_syntax(
                fixed_code
            )

            validation_results.append(
                {
                    "path": path,
                    **result
                }
            )

        else:
            validation_results.append(
                {
                    "path": path,
                    "valid": False,
                    "error_type": None,
                    "message": (
                        f"Validation is not implemented "
                        f"for {path}"
                    ),
                    "line": None,
                    "offset": None
                }
            )

    all_valid = (
        bool(validation_results)
        and all(
            result["valid"]
            for result in validation_results
        )
    )

    return {
        "validation_result": {
            "valid": all_valid,
            "files": validation_results
        }
    }

def review_fix_node(
        state: DebugState
        ) -> dict[str,object]:

    print("[6] REVIEWING FIX")

    fix = state["proposed_fix"]

    result = review_fix(
    original_code=state["code"],
    error=state["error"],
    file_changes=str(
        fix["file_changes"]
    ),
    explanation=fix["explanation"],
    validation_result=str(
        state["validation_result"]
    )
)
    return {
        "final_report": {
            "error_analysis": state["error_analysis"],
            "tool_execution": state["tool_result"],
            "proposed_fix": state["proposed_fix"],
            "validation": state["validation_result"],
            "retrieved_context": state["retrieved_context"],
            "critic": result.model_dump()
        }
    }


graph = StateGraph(DebugState)

graph.add_node(
    "analyze_error",
    analyze_error_node
)

graph.add_node(
    "retrieve_context",
    retrieve_context_node
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

graph.add_conditional_edges(
    "analyze_error",
    route_repository_context,
    {
        "retrieve_context": "retrieve_context",
        "select_tool": "select_tool"
    }
)

graph.add_edge(
    "retrieve_context",
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