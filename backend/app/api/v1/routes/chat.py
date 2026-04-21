from fastapi import APIRouter
from pydantic import BaseModel

from app.services.llm_service import get_ai_response
from app.services.triage_service import analyze_symptoms

router = APIRouter()


# =========================
# 📩 REQUEST MODEL
# =========================
class ChatRequest(BaseModel):
    message: str


# =========================
# 💬 CHAT (NO AUTH + NO DB)
# =========================
@router.post("/")
def chat(req: ChatRequest):
    try:
        # 🧠 AI RESPONSE
        ai_reply = get_ai_response(req.message)

        # 🩺 TRIAGE ANALYSIS
        triage = analyze_symptoms(req.message)

        # 🔥 MERGED RESPONSE
        final_response = f"""
{ai_reply}

-------------------------

📊 Risk Level: {triage['risk']}

🩺 Advice:
{triage['advice']}
"""

        return {
            "user": "guest",
            "message": req.message,
            "response": final_response
        }

    except Exception as e:
        return {"error": str(e)}


# =========================
# 🕘 CHAT HISTORY (TEMP)
# =========================
@router.get("/history")
def get_chat_history():
    return [
        {
            "message": "history disabled",
            "response": "Database removed for deployment",
            "risk": "N/A"
        }
    ]