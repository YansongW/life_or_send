from typing import Optional, Any
import json
from datetime import datetime, timedelta
import aioredis
from config.config import settings

class CacheService:
    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL)
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存数据"""
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None
    
    async def set(
        self,
        key: str,
        value: Any,
        expire_seconds: int = 300
    ):
        """设置缓存数据"""
        await self.redis.set(
            key,
            json.dumps(value),
            ex=expire_seconds
        )
    
    async def delete(self, key: str):
        """删除缓存数据"""
        await self.redis.delete(key)
    
    async def clear_pattern(self, pattern: str):
        """清除匹配模式的所有缓存"""
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)
    
    def get_key(self, *args) -> str:
        """生成缓存key"""
        return ":".join(map(str, args)) 