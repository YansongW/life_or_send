import functools
from typing import Optional
from services.cache_service import CacheService
import logging

logger = logging.getLogger(__name__)

def cache(
    expire_seconds: int = 300,
    prefix: str = "",
    key_builder: Optional[callable] = None
):
    """缓存装饰器"""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cache_service = CacheService()
            
            # 生成缓存key
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                params = f"{args}_{kwargs}"
                cache_key = f"{prefix}:{func.__name__}:{hash(params)}"
            
            # 尝试获取缓存
            cached_data = await cache_service.get(cache_key)
            if cached_data is not None:
                return cached_data
            
            # 执行函数
            result = await func(*args, **kwargs)
            
            # 设置缓存
            await cache_service.set(
                cache_key,
                result,
                expire_seconds=expire_seconds
            )
            
            return result
        return wrapper
    return decorator
