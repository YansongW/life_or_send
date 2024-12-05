from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
import enum
from database.db import Base

class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    wx_open_id = Column(String(64), unique=True, index=True)
    nickname = Column(String(64), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active_at = Column(DateTime, default=datetime.utcnow)