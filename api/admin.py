from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database.db import get_db
from services.export_service import ExportService
from services.analytics_service import AnalyticsService
from dependencies.auth import check_admin_access
from .base import BaseResponse, APIException, APITags

router = APIRouter(prefix="/admin", tags=[APITags.SYSTEM])

@router.get("/export/chat-history")
async def export_chat_history(
    user_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """导出聊天历史"""
    try:
        service = ExportService(db)
        data = await service.export_chat_history_csv(user_id)
        return data
    except Exception as e:
        raise APIException(
            status_code=500,
            code=8001,
            message="Failed to export chat history",
            detail=str(e)
        )

@router.get("/analytics/overview")
async def get_analytics_overview(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """获取系统概览统计"""
    try:
        service = AnalyticsService(db)
        stats = await service.get_daily_usage_stats(days)
        user_stats = await service.get_user_activity_stats()
        response_time = await service.get_response_time_stats()
        
        return BaseResponse(data={
            "daily_stats": stats,
            "user_stats": user_stats,
            "response_time": response_time
        })
    except Exception as e:
        raise APIException(
            status_code=500,
            code=8002,
            message="Failed to get analytics overview",
            detail=str(e)
        ) 