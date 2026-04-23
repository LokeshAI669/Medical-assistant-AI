from fastapi import APIRouter
from app.api.v1.routes import chat, health, auth, triage, reports

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(chat.router, prefix="/chat")
api_router.include_router(health.router, prefix="/health")
api_router.include_router(triage.router, prefix="/triage")
api_router.include_router(reports.router, prefix="/reports")