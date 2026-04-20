from fastapi import APIRouter
from pydantic import BaseModel
from app.services.triage_service import analyze_symptoms

router = APIRouter()

class TriageRequest(BaseModel):
    message: str

@router.post("/")
def triage(req: TriageRequest):
    result = analyze_symptoms(req.message)
    return result