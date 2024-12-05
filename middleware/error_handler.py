from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Union
import traceback
from utils.logger import setup_logger

logger = setup_logger("error_handler")

async def error_handler_middleware(
    request: Request,
    call_next
):
    try:
        return await call_next(request)
    except Exception as e:
        # 记录错误日志
        error_detail = {
            "path": request.url.path,
            "method": request.method,
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        logger.error(f"Request failed: {error_detail}")
        
        # 返回错误响应
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Internal server error",
                "message": str(e)
            }
        )