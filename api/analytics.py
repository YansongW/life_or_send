from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from database.db import get_db
from services.analytics_service import AnalyticsService
from .base import BaseResponse, APIException, APITags

router = APIRouter(prefix="/analytics", tags=[APITags.ANALYTICS])

@router.get("/daily-usage")
async def get_daily_usage(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """获取每日使用统计"""
    try:
        service = AnalyticsService(db)
        stats = await service.get_daily_usage_stats(days)
        return BaseResponse(data=stats)
    except Exception as e:
        raise APIException(
            status_code=500,
            code=6001,
            message="Failed to get daily usage stats",
            detail=str(e)
        )

@router.get("/user-behavior/{user_id}")
async def get_user_behavior(
    user_id: str,
    db: Session = Depends(get_db)
):
    """获取用户行为分析"""
    try:
        service = AnalyticsService(db)
        stats = await service.get_user_behavior_stats(user_id)
        return BaseResponse(data=stats)
    except Exception as e:
        raise APIException(
            status_code=500,
            code=6002,
            message="Failed to get user behavior stats",
            detail=str(e)
        )

@router.get("/response-time")
async def get_response_time_stats(
    db: Session = Depends(get_db)
):
    """获取响应时间统计"""
    try:
        service = AnalyticsService(db)
        stats = await service.get_response_time_stats()
        return BaseResponse(data=stats)
    except Exception as e:
        raise APIException(
            status_code=500,
            code=6003,
            message="Failed to get response time stats",
            detail=str(e)
        ) 