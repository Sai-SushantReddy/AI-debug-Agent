from pydantic import BaseModel

from app.core.llm import llm


class CriticResult(BaseModel):
    accepted: bool
    issues: list[str]
    feedback: str


structured_llm = llm.with_structured_output(
    CriticResult,
    method="json_mode"
)


def review_fix(
    original_code: str,
    error: str,
    file_changes: str,
    explanation: str,
    validation_result: str
) -> CriticResult:

    prompt = f"""
    You are a senior software engineer reviewing a proposed bug fix.

    Original Code:
    {original_code}

    Original Error:
    {error}

    Proposed Repository File Changes:
    {file_changes}

    Fix Explanation:
    {explanation}

    Deterministic Validation Result:
    {validation_result}

    Review the proposed fix.

    Return ONLY a valid JSON object.

The JSON must follow exactly this structure:

{{
    "accepted": true,
    "issues": [],
    "feedback": "concise technical review"
}}

Important JSON Rules:
- accepted MUST be a JSON boolean.
- issues MUST be a JSON array of strings.
- If there are no issues, return [].
- Do not return issues as a string.
- Do not wrap the JSON in markdown.

    Critic rules:
- Determine whether the proposed file changes address the root cause.
- Check whether the correct repository file is being modified.
- Use the validation result as deterministic evidence.
- Identify technical correctness, syntax, dependency, runtime,
  or logic issues only.
- Do not request explanatory comments unless required for correctness.
- If there are no issues, return an empty issues list.
- Never return "None" or "No issues" inside the issues list.
- Accept only if the fix directly addresses the reported error
  without introducing obvious new problems.


    Determine:
    - whether the fix should be accepted
    - any remaining issues
    - concise technical feedback
    """

    return structured_llm.invoke(prompt)