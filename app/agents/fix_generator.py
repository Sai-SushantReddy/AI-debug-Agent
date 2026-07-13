from pydantic import BaseModel

from app.core.llm import llm


class FixProposal(BaseModel):
    explanation: str
    fixed_code: str
    changes: list[str]
    confidence: float


structured_llm = llm.with_structured_output(
    FixProposal
)


def generate_fix(
    code: str,
    error: str,
    language: str,
    error_analysis: str
) -> FixProposal:

    prompt = f"""
    You are an expert software debugging engineer.

    Generate a fix for the following code error.

    Language:
    {language}

    Code:
    {code}

    Error:
    {error}

    Error Analysis:
    {error_analysis}

Provide:
- an explanation of the fix
- the complete fixed code
- a list of concise human-readable descriptions of each change made
- each change item must explain exactly one modification
- do not return code lines or nested list representations in the changes field
- confidence score between 0 and 1
    """

    return structured_llm.invoke(prompt)