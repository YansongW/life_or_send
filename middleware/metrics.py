from fastapi import Request
import time
from prometheus_client import Counter, Histogram
import logging

logger = logging.getLogger(__name__)

# 定义指标
REQUEST_COUNT = Counter(
    'http_request_count',
    'HTTP Request Count',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_latency_seconds',
    'HTTP Request Latency',
    ['method', 'endpoint']
)

async def metrics_middleware(request: Request, call_next):
    """性能监控中间件"""
    start_time = time.time()
    
    response = await call_next(request)
    
    # 记录请求数
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    # 记录响应时间
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(time.time() - start_time)
    
    return response 