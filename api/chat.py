from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database.db import get_db
from models.message import Message
from pydantic import BaseModel, Field
from .base import BaseResponse, PaginationParams, APIException

router = APIRouter(prefix="/api/chat", tags=["chat"])

class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None

class MessageResponse(BaseModel):
    id: int
    content: str
    message_type: str
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/history", response_model=List[MessageResponse])
async def get_chat_history(
    user_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    keyword: Optional[str] = None,
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    db: Session = Depends(get_db)
):
    """获取聊天历史记录"""
    query = db.query(Message).filter(Message.user_id == user_id)
    
    if start_time:
        query = query.filter(Message.created_at >= start_time)
    if end_time:
        query = query.filter(Message.created_at <= end_time)
    if keyword:
        query = query.filter(Message.content.contains(keyword))
    
    total = query.count()
    messages = query.order_by(Message.created_at.desc())\
        .offset((page - 1) * page_size)\
        .limit(page_size)\
        .all()
    
    return messages 

@router.post("/send", response_model=BaseResponse[MessageResponse])
async def send_message(
    data: MessageCreate,
    user_id: str,
    db: Session = Depends(get_db)
):
    try:
        chat_service = ChatService(db)
        response = await chat_service.handle_message(
            user_id=user_id,
            content=data.content,
            session_id=data.session_id
        )
        return BaseResponse(data=response)
    except ValueError as e:
        raise APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code=4001,
            message="Invalid request",
            detail=str(e)
        )
    except Exception as e:
        raise APIException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code=5001,
            message="Internal server error",
            detail=str(e)
        ) 