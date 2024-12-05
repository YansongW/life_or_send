from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from services.monitor_service import SystemMonitor
from services.queue_service import QueueService
import aioredis
from config.config import settings
from .base import BaseResponse, APIException, APITags

router = APIRouter(prefix="/health", tags=[APITags.SYSTEM])

@router.get("")
async def health_check(db: Session = Depends(get_db)):
    """系统健康检查"""
    health_status = {
        "status": "healthy",
        "services": {
            "database": "healthy",
            "redis": "healthy",
            "rabbitmq": "healthy",
            "system": "healthy"
        }
    }
    
    try:
        # 检查数据库
        db.execute("SELECT 1")
    except Exception as e:
        health_status["services"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    try:
        # 检查Redis
        redis = await aioredis.from_url(settings.REDIS_URL)
        await redis.ping()
        await redis.close()
    except Exception as e:
        health_status["services"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    try:
        # 检查RabbitMQ
        queue_service = QueueService()
        await queue_service.connect()
        await queue_service.close()
    except Exception as e:
        health_status["services"]["rabbitmq"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    try:
        # 检查系统资源
        monitor = SystemMonitor()
        system_status = await monitor.check_system_resources()
        if any(status["alert"] for status in system_status.values()):
            health_status["services"]["system"] = "warning: resource usage high"
            health_status["status"] = "warning"
    except Exception as e:
        health_status["services"]["system"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    return BaseResponse(data=health_status)

@router.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)):
    """获取系统指标"""
    try:
        monitor = SystemMonitor()
        metrics = await monitor.check_system_resources()
        return BaseResponse(data=metrics)
    except Exception as e:
        raise APIException(
            status_code=500,
            code=7001,
            message="Failed to get system metrics",
            detail=str(e)
        ) 