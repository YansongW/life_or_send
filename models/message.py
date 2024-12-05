from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), index=True)
    session_id = Column(String(64), ForeignKey("chat_sessions.session_id"), index=True)
    content = Column(Text)
    message_type = Column(String(20))  # 'user' 或 'bot'
    created_at = Column(DateTime, default=datetime.utcnow)
    vector_id = Column(String(64), nullable=True)  # 向量数据库中的ID
    
    # 建立与会话的关系
    session = relationship("ChatSession", back_populates="messages")