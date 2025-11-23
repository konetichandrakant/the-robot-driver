from fastapi import FastAPI
from src.api.routers.automation import router as automation_router

app = FastAPI(title="The Robot Driver API")

app.include_router(automation_router, prefix="/api", tags=["automation"])
