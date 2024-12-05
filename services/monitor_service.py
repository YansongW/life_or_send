import psutil
from datetime import datetime
import logging
from config.config import settings

logger = logging.getLogger(__name__)

class SystemMonitor:
    def __init__(self):
        self.alert_thresholds = {
            "cpu": 80.0,  # CPU使用率阈值
            "memory": 85.0,  # 内存使用率阈值
            "disk": 90.0  # 磁盘使用率阈值
        }
    
    async def check_system_resources(self) -> Dict:
        """检查系统资源使用情况"""
        # CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # 内存使用率
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # 磁盘使用率
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        
        status = {
            "cpu": {
                "usage": cpu_percent,
                "alert": cpu_percent > self.alert_thresholds["cpu"]
            },
            "memory": {
                "usage": memory_percent,
                "alert": memory_percent > self.alert_thresholds["memory"]
            },
            "disk": {
                "usage": disk_percent,
                "alert": disk_percent > self.alert_thresholds["disk"]
            }
        }
        
        # 记录告警
        for resource, data in status.items():
            if data["alert"]:
                logger.warning(
                    f"Resource alert: {resource} usage at {data['usage']}%"
                )
        
        return status
