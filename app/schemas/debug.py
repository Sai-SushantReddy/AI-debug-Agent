from pydantic import BaseModel


class DebugRequest(BaseModel):
    code: str
    error: str
    language: str


class DebugResponse(BaseModel):
    error_type: str
    root_cause: str
    explanation: str
    suggested_fix: str
    fixed_code: str
    confidence: float