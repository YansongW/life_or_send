from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.db import get_db
import logging

logger = logging.getLogger(__name__)

class ScheduledTasks:
    def __init__(self, scheduler: AsyncIOScheduler, db: Session):
        self.scheduler = scheduler
        self.db = db
    
    async def cleanup_expired_sessions(self):
        """清理过期会话"""
        try:
            expiry_time = datetime.utcnow() - timedelta(days=7)
            result = await self.db.execute(
                """
                UPDATE chat_sessions 
                SET is_active = FALSE 
                WHERE updated_at < :expiry_time 
                AND is_active = TRUE
                """,
                {"expiry_time": expiry_time}
            )
            logger.info(f"Cleaned up {result.rowcount} expired sessions")
        except Exception as e:
            logger.error(f"Failed to cleanup sessions: {e}")
    
    async def generate_daily_statistics(self):
        """生成每日统计"""
        try:
            yesterday = datetime.utcnow() - timedelta(days=1)
            stats = await self.db.execute(
                """
                SELECT 
                    COUNT(DISTINCT session_id) as total_sessions,
                    COUNT(*) as total_messages,
                    COUNT(CASE WHEN message_type = 'user' THEN 1 END) as user_messages,
                    COUNT(CASE WHEN message_type = 'bot' THEN 1 END) as bot_messages
                FROM messages
                WHERE DATE(created_at) = DATE(:date)
                """,
                {"date": yesterday}
            )
            logger.info(f"Generated daily statistics: {stats.first()}")
        except Exception as e:
            logger.error(f"Failed to generate statistics: {e}")

def setup_scheduled_tasks(scheduler: AsyncIOScheduler, db: Session):
    tasks = ScheduledTasks(scheduler, db)
    
    # 添加定时任务
    scheduler.add_job(
        tasks.cleanup_expired_sessions,
        'interval',
        minutes=5,
        id='cleanup_sessions'
    )
    
    scheduler.add_job(
        tasks.generate_daily_statistics,
        'cron',
        hour=0,
        minute=5,
        id='daily_stats'
    ) 