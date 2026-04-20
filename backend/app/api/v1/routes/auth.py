from fastapi import APIRouter
from pydantic import BaseModel
from app.db.session import SessionLocal
from app.db.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str


# 🔥 REGISTER
@router.post("/register")
def register(req: RegisterRequest):
    db = SessionLocal()

    user = User(
        email=req.email,
        password=hash_password(req.password)
    )

    db.add(user)
    db.commit()
    db.close()

    return {"message": "User registered successfully"}


# 🔥 LOGIN
@router.post("/login")
def login(req: LoginRequest):
    db = SessionLocal()

    user = db.query(User).filter(User.email == req.email).first()

    if not user or not verify_password(req.password, user.password):
        return {"error": "Invalid credentials"}

    token = create_access_token({"sub": user.email})

    db.close()

    return {"access_token": token}