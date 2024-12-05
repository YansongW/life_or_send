from typing import List, Optional
from sqlalchemy.orm import Session
from models.chat_session import ChatSession
import uuid
import json
from datetime import datetime
from services.cache_service import CacheService

class SessionService:
    def __init__(self, db: Session):
        self.db = db
        self.cache = CacheService()
    
    async def create_session(self, user_id: str, title: str = None) -> ChatSession:
        """创建新的会话"""
        session = ChatSession(
            user_id=user_id,
            session_id=str(uuid.uuid4()),
            title=title or f"对话 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            context=json.dumps([])  # 初始化空上下文
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
    
    async def get_user_sessions(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[ChatSession]:
        """获取用户的会话列表"""
        return self.db.query(ChatSession)\
            .filter(ChatSession.user_id == user_id)\
            .filter(ChatSession.is_active == True)\
            .order_by(ChatSession.updated_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    async def get_session(self, session_id: str) -> Optional[ChatSession]:
        """获取特定会话"""
        # 尝试从缓存获取
        cache_key = self.cache.get_key("session", session_id)
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return ChatSession(**cached_data)
        
        # 从数据库获取
        session = self.db.query(ChatSession)\
            .filter(ChatSession.session_id == session_id)\
            .first()
        
        # 设置缓存
        if session:
            await self.cache.set(
                cache_key,
                session.__dict__,
                expire_seconds=300
            )
        
        return session
    
    async def update_context(
        self,
        session_id: str,
        user_message: str,
        bot_message: str
    ) -> ChatSession:
        """更新会话上下文"""
        session = await self.get_session(session_id)
        if not session:
            raise ValueError("Session not found")
        
        context = json.loads(session.context)
        context.append({"role": "user", "content": user_message})
        context.append({"role": "assistant", "content": bot_message})
        
        # 只保留最近的10轮对话
        if len(context) > 20:
            context = context[-20:]
        
        session.context = json.dumps(context)
        session.updated_at = datetime.utcnow()
        self.db.commit()
        return session
    
    async def clear_context(self, session_id: str) -> ChatSession:
        """清除会话上下文"""
        session = await self.get_session(session_id)
        if not session:
            raise ValueError("Session not found")
        
        session.context = json.dumps([])
        self.db.commit()
        return session
    
    async def delete_session(self, session_id: str):
        """删除会话"""
        session = await self.get_session(session_id)
        if not session:
            raise ValueError("Session not found")
        
        session.is_active = False
        self.db.commit()
        return session
    
    async def get_all_sessions(
        self,
        skip: int = 0,
        limit: int = 20
    ) -> List[ChatSession]:
        """获取所有会话（管理员用）"""
        return self.db.query(ChatSession)\
            .order_by(ChatSession.updated_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    async def search_sessions(
        self,
        user_id: str,
        keyword: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[ChatSession]:
        """搜索会话"""
        query = self.db.query(ChatSession)\
            .filter(ChatSession.is_active == True)
        
        # 非管理员只能搜索自己的会话
        if user_id:
            query = query.filter(ChatSession.user_id == user_id)
        
        # 关键词搜索
        if keyword:
            query = query.join(Message)\
                .filter(Message.content.contains(keyword))\
                .group_by(ChatSession.id)
        
        # 时间范围
        if start_date:
            query = query.filter(ChatSession.created_at >= start_date)
        if end_date:
            query = query.filter(ChatSession.created_at <= end_date)
        
        # 排序和分页
        total = query.count()
        sessions = query.order_by(ChatSession.updated_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
        
        return sessions, total 