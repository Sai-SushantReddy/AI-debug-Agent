from fastapi import FastAPI

from app.api.debug import router as debug_router

app = FastAPI(
    title="AI Debug Agent",
    version="2.0.0"
)

app.include_router(debug_router)