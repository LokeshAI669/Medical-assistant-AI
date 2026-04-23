from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ Import routers
from app.api.v1.api import api_router

# ✅ Import DB
from app.db.session import Base, engine

# ✅ Import models (VERY IMPORTANT)
from app.db.models.user import User


# =========================
# 🚀 CREATE APP
# =========================
app = FastAPI(title="Medical AI Assistant")


# =========================
# 🌐 ENABLE CORS (FIX FRONTEND ERROR)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# 💾 CREATE DATABASE TABLES
# =========================
Base.metadata.create_all(bind=engine)


# =========================
# 🏠 ROOT API
# =========================
@app.get("/")
def root():
    return {"message": "Medical AI Backend Running 🚀"}


# =========================
# 🔗 INCLUDE ROUTES
# =========================
app.include_router(api_router, prefix="/api/v1")