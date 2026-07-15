from pydantic import BaseModel

from app.core.llm import llm


class ErrorAnalysis(BaseModel):
    error_type: str
    probable_cause: str
    affected_line: int | None
    severity: str
    requires_repository_context: bool


structured_llm = llm.with_structured_output(
    ErrorAnalysis,
    method="json_mode"
)


def analyze_error(
    code: str,
    error: str,
    language: str
) -> ErrorAnalysis:

    prompt = f"""
You are an expert software debugging engineer.

Analyze the reported code error.

Language:
{language}

Code:
{code}

Reported Error:
{error}

Return ONLY a valid JSON object.

The JSON must follow exactly this structure:

{{
    "error_type": "KeyError",
    "probable_cause": "concise technical cause",
    "affected_line": 3,
    "severity": "error",
    "requires_repository_context": true
}}

Rules:
- affected_line MUST be an integer or null.
- Never return text in affected_line.
- If the exact line cannot be determined, return null.
- requires_repository_context MUST be a JSON boolean.
- Use true or false without quotes.
- Never return "True" or "False" as strings.
- Set requires_repository_context to true when resolving the root cause may require another project file, internal module, configuration file, or repository symbol.
- Do not wrap the JSON in markdown.
- Do not return additional fields.
"""

    return structured_llm.invoke(prompt)