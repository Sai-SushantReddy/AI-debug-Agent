from fastapi import APIRouter

from app.schemas.debug import DebugRequest

router = APIRouter(
    prefix="/debug",
    tags=["Debug"]
)


@router.post("")
async def debug_code(request: DebugRequest):

    return {
        "message": "Debug workflow will run here"
    }