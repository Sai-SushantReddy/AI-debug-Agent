from fastapi import APIRouter

from app.schemas.debug import DebugRequest
from app.workflows.debug_graph import debug_graph

router = APIRouter(
    prefix="/debug",
    tags=["Debug"]
)


@router.post("")
async def debug_code(request: DebugRequest):
    result = debug_graph.invoke(
        {
            "code": request.code,
            "error": request.error,
            "language": request.language,
            "retry_count": 0
        }
    )
    return result["final_report"]