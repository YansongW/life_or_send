from fastapi import Request, HTTPException, status
from typing import Dict, Tuple
from datetime import datetime, timedelta
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
    
    def _clean_old_requests(self, key: str):
        """清理超过1分钟的请求记录"""
        current_time = time.time()
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if current_time - req_time < 60
        ]
    
    def is_allowed(self, key: str) -> Tuple[bool, float]:
        """检查请求是否允许"""
        self._clean_old_requests(key)
        
        if len(self.requests[key]) >= self.requests_per_minute:
            oldest_request = self.requests[key][0]
            return False, 60 - (time.time() - oldest_request)
        
        self.requests[key].append(time.time())
        return True, 0

async def rate_limit_middleware(
    request: Request,
    call_next,
    requests_per_minute: int = 60
):
    """速率限制中间件"""
    limiter = getattr(request.app.state, 'rate_limiter', None)
    if limiter is None:
        limiter = RateLimiter(requests_per_minute)
        request.app.state.rate_limiter = limiter
    
    # 使用IP和路径组合作为限制key
    key = f"{request.client.host}:{request.url.path}"
    allowed, wait_time = limiter.is_allowed(key)
    
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "code": 4029,
                "message": "Too many requests",
                "detail": f"Please wait {wait_time:.1f} seconds"
            }
        )
    
    return await call_next(request) 