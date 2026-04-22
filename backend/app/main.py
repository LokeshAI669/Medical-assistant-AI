from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router

# Create FastAPI app
app = FastAPI(title="Medical AI Assistant")

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Medical AI Backend Running 🚀"}

# Include routes
app.include_router(api_router, prefix="/api/v1")