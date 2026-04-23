from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def triage():
    return {"message": "Triage working"}