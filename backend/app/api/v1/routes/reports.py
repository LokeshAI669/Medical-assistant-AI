from fastapi import APIRouter, Depends
from app.core.security import get_current_user

router = APIRouter()

@router.get("/")
def get_reports(user: str = Depends(get_current_user)):
    return {
        "user": user,
        "report": "Health stable, low risk"
    }