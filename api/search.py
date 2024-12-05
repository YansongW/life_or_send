from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database.db import get_db
from services.search_service import SearchService
from models.message import Message
from .base import BaseResponse, PaginationParams, APIException, APITags

router = APIRouter(prefix="/search", tags=[APITags.SEARCH])

@router.get("/messages", response_model=BaseResponse[List[Message]])
async def search_messages(
    keyword: str = Query(..., min_length=1, max_length=100),
    user_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db)
):
    """搜索消息"""
    try:
        service = SearchService(db)
        messages = await service.search_by_content(
            keyword=keyword,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            skip=pagination.get_skip(),
            limit=pagination.page_size
        )
        return BaseResponse(data=messages)
    except Exception as e:
        raise APIException(
            status_code=500,
            code=5001,
            message="Search failed",
            detail=str(e)
        )

@router.get("/statistics")
async def get_statistics(
    user_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """获取统计信息"""
    try:
        service = SearchService(db)
        stats = await service.get_session_statistics(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        return BaseResponse(data=stats)
    except Exception as e:
        raise APIException(
            status_code=500,
            code=5002,
            message="Failed to get statistics",
            detail=str(e)
        ) 