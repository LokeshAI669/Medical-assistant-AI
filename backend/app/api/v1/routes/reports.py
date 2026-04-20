from fastapi import APIRouter, UploadFile, File, Depends
from app.utils.file_parser import extract_text_from_pdf
from app.services.llm_service import get_ai_response
from app.core.security import get_current_user

router = APIRouter()

@router.post("/")
async def analyze_report(
    file: UploadFile = File(...),
    user: str = Depends(get_current_user)
):
    try:
        contents = await file.read()

        with open("temp.pdf", "wb") as f:
            f.write(contents)

        text = extract_text_from_pdf("temp.pdf")

        prompt = f"""
You are a medical assistant.

Explain this medical report in simple language:

{text}
"""

        ai_response = get_ai_response(prompt)

        return {
            "message": "Report analyzed",
            "analysis": ai_response
        }

    except Exception as e:
        return {"error": str(e)}