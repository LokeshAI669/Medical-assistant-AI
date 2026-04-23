from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.security import hash_password, verify_password, create_access_token
from app.db.session import SessionLocal
from app.db.models.user import User

router = APIRouter()

class UserRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(req: UserRequest):
    db = SessionLocal()

    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User exists")

    new_user = User(
        email=req.email,
        password=hash_password(req.password)
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {"message": "Registered successfully"}


@router.post("/login")
def login(req: UserRequest):
    db = SessionLocal()

    user = db.query(User).filter(User.email == req.email).first()

    if not user or not verify_password(req.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    db.close()

    return {"access_token": token}