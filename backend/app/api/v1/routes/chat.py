from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services.llm_service import get_ai_response
from app.services.triage_service import analyze_symptoms
from app.db.session import SessionLocal
from app.db.models.chat import Chat
from app.core.security import get_current_user

router = APIRouter()


# =========================
# 📩 REQUEST MODEL
# =========================
class ChatRequest(BaseModel):
    message: str


# =========================
# 💬 CHAT (PROTECTED)
# =========================
@router.post("/")
def chat(
    req: ChatRequest,
    user: str = Depends(get_current_user)  # 🔐 PROTECTED ROUTE
):
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
            "user": user,  # 🔐 shows logged-in user
            "message": req.message,
            "response": final_response
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()


# =========================
# 🕘 CHAT HISTORY
# =========================
@router.get("/history")
def get_chat_history(user: str = Depends(get_current_user)):
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