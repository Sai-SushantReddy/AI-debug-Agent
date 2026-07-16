from pydantic import BaseModel

from app.core.llm import llm


class FileChange(BaseModel):
    path: str
    fixed_code: str
    description: str


class FixProposal(BaseModel):
    explanation: str
    file_changes: list[FileChange]
    confidence: float


structured_llm = llm.with_structured_output(
    FixProposal,
    method="json_mode"
)


def generate_fix(
    code: str,
    error: str,
    language: str,
    error_analysis: str,
    tool_result: str,
    retrieved_context: str,
    previous_feedback: str
) -> FixProposal:

    prompt = f"""
You are an expert software debugging engineer.

Generate a repository-aware fix for the reported error.

Language:
{language}

Code where the error was observed:
{code}

Error:
{error}

Error Analysis:
{error_analysis}

Deterministic Debugging Tool Result:
{tool_result}

Retrieved Repository Context:
{retrieved_context}

Previous Critic Feedback:

{previous_feedback}

If this is not empty,
improve the previous fix by addressing every issue raised.

Do not repeat the same incorrect solution.
Identify the actual root-cause file and propose the required
repository file changes.

Rules:
- Modify the root-cause file, not merely the calling code.
- Use only file paths present in the repository context.
- Do not invent file paths.
- Return only files that require modification.
- Each file change must contain the complete corrected code.
- Ensure the proposed change directly addresses the error.

Return ONLY a valid JSON object.

The JSON must follow exactly this structure:

{{
    "explanation": "concise explanation of root cause and fix",
    "file_changes": [
        {{
            "path": "config.py",
            "fixed_code": "complete corrected file code",
            "description": "concise description of the modification"
        }}
    ],
    "confidence": 0.95
}}

Important JSON rules:
- file_changes MUST be a JSON array.
- file_changes MUST NOT be a string.
- Each file_changes item MUST be a JSON object.
- Do not wrap the JSON in markdown.
- Do not use Python list syntax.
- Do not return a top-level fixed_code field.
- Do not return a changes field.
- Do not return repository_context.
"""

    return structured_llm.invoke(prompt)