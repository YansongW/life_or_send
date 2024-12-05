from fastapi import HTTPException, status, APIRouter as FastAPIRouter
from pydantic import BaseModel
from typing import Optional, Generic, TypeVar, Dict, Any
from datetime import datetime

T = TypeVar('T')

class ErrorResponse(BaseModel):
    code: int
    message: str
    detail: Optional[str] = None

class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20
    
    def get_skip(self) -> int:
        return (self.page - 1) * self.page_size

class BaseResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    error: Optional[ErrorResponse] = None
    timestamp: datetime = datetime.utcnow()

class APIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        code: int,
        message: str,
        detail: Optional[str] = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "code": code,
                "message": message,
                "detail": detail
            }
        ) 

class APIRouter(FastAPIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = f"/api/v1{kwargs.get('prefix', '')}"

class APITags:
    CHAT = "聊天"
    SESSION = "会话"
    SEARCH = "搜索"
    ANALYTICS = "统计"
    SYSTEM = "系统"