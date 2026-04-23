from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.llm_service import get_ai_response
from app.services.triage_service import analyze_symptoms
from app.core.security import get_current_user

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

chat_history = []

@router.post("/")
def chat(req: ChatRequest, user: str = Depends(get_current_user)):
    ai_reply = get_ai_response(req.message)
    triage = analyze_symptoms(req.message)

    final = f"{ai_reply}\n\nRisk: {triage['risk']}\nAdvice: {triage['advice']}"

    chat_history.append({
        "user": user,
        "message": req.message,
        "response": final
    })

    return {"response": final}

@router.get("/history")
def history(user: str = Depends(get_current_user)):
    return chat_history