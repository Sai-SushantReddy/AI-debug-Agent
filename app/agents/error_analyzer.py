from pydantic import BaseModel
from app.core.llm import llm

class ErrorAnalysis(BaseModel):

    error_type: str

    probable_cause: str

    affected_line: int | None

    severity: str

    requires_repository_context: bool
    
structured_llm = llm.with_structured_output(
    ErrorAnalysis
)

def analyze_error(
    code: str,
    error: str,
    language: str
) -> ErrorAnalysis:

    prompt = f"""
    You are a software debugging specialist.

    Analyze the following error.

    Language:
    {language}

    Code:
    {code}

    Error:
    {error}

    Identify:
    - the error type
    - probable root cause
    - affected line if identifiable
    - severity
    - whether repository context is required
    """
    return structured_llm.invoke(prompt)