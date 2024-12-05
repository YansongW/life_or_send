from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from config.config import settings
import logging

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self):
        jobstores = {
            'default': SQLAlchemyJobStore(url=settings.DATABASE_URL)
        }
        executors = {
            'default': ThreadPoolExecutor(20)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }
        
        self.scheduler = AsyncIOScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults
        )
    
    async def start(self):
        """启动调度器"""
        try:
            self.scheduler.start()
            logger.info("Scheduler started")
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")
            raise
    
    async def add_job(self, *args, **kwargs):
        """添加定时任务"""
        return self.scheduler.add_job(*args, **kwargs)
    
    async def remove_job(self, job_id):
        """移除定时任务"""
        self.scheduler.remove_job(job_id)
    
    async def shutdown(self):
        """关闭调度器"""
        self.scheduler.shutdown()
