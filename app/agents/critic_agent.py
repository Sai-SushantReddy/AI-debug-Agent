from pydantic import BaseModel

from app.core.llm import llm


class CriticResult(BaseModel):
    accepted: bool
    issues: list[str]
    feedback: str


structured_llm = llm.with_structured_output(
    CriticResult
)


def review_fix(
    original_code: str,
    error: str,
    fixed_code: str,
    explanation: str
) -> CriticResult:

    prompt = f"""
    You are a senior software engineer reviewing a proposed bug fix.

    Original Code:
    {original_code}

    Original Error:
    {error}

    Proposed Fixed Code:
    {fixed_code}

    Fix Explanation:
    {explanation}

    Review the proposed fix.

    Determine:
    - whether the fix should be accepted
    - any remaining issues
    - feedback for improving the fix
    """

    return structured_llm.invoke(prompt)