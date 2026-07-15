from typing import TypedDict


class ErrorAnalysisState(TypedDict):
    error_type: str
    probable_cause: str
    affected_line: int | None
    severity: str
    requires_repository_context: bool


class SyntaxCheckResult(TypedDict):
    valid: bool
    error_type: str | None
    message: str | None
    line: int | None
    offset: int | None


class DependencyCheckResult(TypedDict):
    imports: list[str]
    missing_dependencies: list[str]
    valid: bool


class GenericToolResult(TypedDict):
    message: str


class ToolResultState(TypedDict):
    tool: str | None
    result: (
        SyntaxCheckResult
        | DependencyCheckResult
        | GenericToolResult
    )

class FileChangeState(TypedDict):
    path: str
    fixed_code: str
    description: str

class FixProposalState(TypedDict):
    explanation: str
    file_changes: list[FileChangeState]
    confidence: float


class CriticResultState(TypedDict):
    accepted: bool
    issues: list[str]
    feedback: str


class RepositoryFileState(TypedDict):
    path: str
    content: str


class RetrievedContextState(TypedDict):
    path: str
    symbol: str
    chunk_type: str
    content: str


class FinalReportState(TypedDict):
    error_analysis: ErrorAnalysisState
    tool_execution: ToolResultState
    proposed_fix: FixProposalState
    validation: SyntaxCheckResult
    retrieved_context: list[RetrievedContextState]
    critic: CriticResultState

class FileValidationState(TypedDict):
    path: str
    valid: bool
    error_type: str | None
    message: str | None
    line: int | None
    offset: int | None


class ValidationResultState(TypedDict):
    valid: bool
    files: list[FileValidationState]

class DebugState(TypedDict):
    code: str
    error: str
    language: str

    project_files: list[RepositoryFileState]

    error_analysis: ErrorAnalysisState
    retrieved_context: list[RetrievedContextState]
    tool_result: ToolResultState
    proposed_fix: FixProposalState
    validation_result: SyntaxCheckResult
    final_report: FinalReportState

    retry_count: int