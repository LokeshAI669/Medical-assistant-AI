from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    response = Column(String)
    risk = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)