from fastapi import FastAPI
from api import wechat, chat, search, analytics, health
from database.db import engine, Base
from middleware.error_handler import error_handler_middleware
from middleware.metrics import metrics_middleware
from services.scheduler_service import SchedulerService
from utils.logger import setup_logger
from prometheus_client import make_asgi_app

logger = setup_logger("main")
scheduler = SchedulerService()

app = FastAPI()

# 添加中间件
app.middleware("http")(error_handler_middleware)
app.middleware("http")(metrics_middleware)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 注册路由
app.include_router(wechat.router)
app.include_router(chat.router)
app.include_router(search.router)
app.include_router(analytics.router)
app.include_router(health.router)

# 添加监控指标endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    await scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down...")
    await scheduler.shutdown()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 