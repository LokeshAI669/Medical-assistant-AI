from fastapi import APIRouter
from pydantic import BaseModel

from app.services.llm_service import get_ai_response
from app.services.triage_service import analyze_symptoms
from app.db.session import SessionLocal
from app.db.models.chat import Chat

router = APIRouter()


# =========================
# 📩 REQUEST MODEL
# =========================
class ChatRequest(BaseModel):
    message: str


# =========================
# 💬 CHAT (NO AUTH)
# =========================
@router.post("/")
def chat(req: ChatRequest):
    db = SessionLocal()

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

        # 💾 SAVE TO DATABASE
        new_chat = Chat(
            message=req.message,
            response=final_response,
            risk=triage["risk"]
        )

        db.add(new_chat)
        db.commit()

        return {
            "user": "guest",   # ✅ no auth
            "message": req.message,
            "response": final_response
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()


# =========================
# 🕘 CHAT HISTORY (NO AUTH)
# =========================
@router.get("/history")
def get_chat_history():
    db = SessionLocal()

    try:
        chats = db.query(Chat).order_by(Chat.id.desc()).all()

        result = []
        for chat in chats:
            result.append({
                "message": chat.message,
                "response": chat.response,
                "risk": chat.risk
            })

        return result

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()