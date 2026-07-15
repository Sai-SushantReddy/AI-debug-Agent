from pydantic import BaseModel,Field

class RepositoryFile(BaseModel):
    path: str
    content: str


class DebugRequest(BaseModel):
    code: str
    error: str
    language: str
    project_files: list[RepositoryFile] = Field(
        default_factory=list
    )
    
class DebugResponse(BaseModel):
    error_type: str
    root_cause: str
    explanation: str
    suggested_fix: str
    fixed_code: str
    confidence: float