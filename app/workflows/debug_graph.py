from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.agents.error_analyzer import analyze_error
from app.agents.fix_generator import generate_fix
from app.agents.critic_agent import review_fix

class DebugState(TypedDict):
    code: str
    error: str
    language: str

    error_analysis: str
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


def generate_fix_node(state: DebugState):

    print("[2] GENERATING FIX")

    result = generate_fix(
        code=state["code"],
        error=state["error"],
        language=state["language"],
        error_analysis=str(
            state["error_analysis"]
        )
    )

    return {
        "proposed_fix": result.model_dump()
    }


def validate_fix_node(state: DebugState):

    print("[3] VALIDATING FIX")

    return {
        "validation_result": {
            "valid": True
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