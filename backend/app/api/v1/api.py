from fastapi import APIRouter
from app.api.v1.routes import chat, health
from app.api.v1.routes import triage
from app.api.v1.routes import reports
api_router = APIRouter()

api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(triage.router, prefix="/triage", tags=["Triage"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])