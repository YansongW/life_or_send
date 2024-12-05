from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database.db import get_db
from services.session_service import SessionService
from models.chat_session import ChatSession
from .base import BaseResponse, PaginationParams, APIException, APITags

router = APIRouter(prefix="/sessions", tags=[APITags.SESSION])

@router.post("", response_model=BaseResponse[ChatSession])
async def create_session(
    user_id: str,
    title: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """创建新会话"""
    try:
        service = SessionService(db)
        session = await service.create_session(user_id, title)
        return BaseResponse(data=session)
    except Exception as e:
        raise APIException(
            status_code=500,
            code=4001,
            message="Failed to create session",
            detail=str(e)
        )

@router.get("", response_model=BaseResponse[List[ChatSession]])
async def get_user_sessions(
    user_id: str,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db)
):
    """获取用户会话列表"""
    try:
        service = SessionService(db)
        sessions = await service.get_user_sessions(
            user_id,
            pagination.get_skip(),
            pagination.page_size
        )
        return BaseResponse(data=sessions)
    except Exception as e:
        raise APIException(
            status_code=500,
            code=4002,
            message="Failed to get sessions",
            detail=str(e)
        )

@router.delete("/{session_id}")
async def delete_session(
    session_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):
    """删除会话"""
    try:
        service = SessionService(db)
        await service.delete_session(session_id)
        return BaseResponse()
    except Exception as e:
        raise APIException(
            status_code=500,
            code=4003,
            message="Failed to delete session",
            detail=str(e)
        ) 