from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.db.base import Base
from app.db.session import engine

# Create FastAPI app
app = FastAPI(title="Medical AI Assistant")

# ✅ Enable CORS (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create DB tables
Base.metadata.create_all(bind=engine)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Medical AI Backend Running 🚀"}

# Include all routes
app.include_router(api_router, prefix="/api/v1")