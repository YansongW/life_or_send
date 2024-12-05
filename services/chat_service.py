from typing import List, Optional
from sqlalchemy.orm import Session
from models.message import Message
from models.user import User
from services.ai_service import AIService
from services.vector_service import VectorService
import json

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()
        self.vector_service = VectorService()
    
    async def handle_message(
        self,
        user_id: str,
        content: str,
        session_id: str = None
    ) -> str:
        """处理用户消息"""
        from .session_service import SessionService
        session_service = SessionService(self.db)
        
        # 如果没有指定session_id，创建新会话
        if not session_id:
            session = await session_service.create_session(user_id)
            session_id = session.session_id
        else:
            session = await session_service.get_session(session_id)
            if not session:
                raise ValueError("Invalid session ID")
        
        # 获取会话上下文
        context = json.loads(session.context) if session.context else []
        
        # 调用AI服务获取回复
        response = await self.ai_service.chat(
            user_id=user_id,
            message=content,
            context=context,
            topic=session.title
        )
        
        # 保存消息记录
        message = Message(
            user_id=user_id,
            content=content,
            message_type='user',
            session_id=session_id
        )
        self.db.add(message)
        
        bot_message = Message(
            user_id=user_id,
            content=response,
            message_type='bot',
            session_id=session_id
        )
        self.db.add(bot_message)
        
        # 更新会话上下文
        await session_service.update_context(
            session_id=session_id,
            user_message=content,
            bot_message=response
        )
        
        self.db.commit()
        
        # 添加到知识库
        await self.vector_service.add_conversation(
            user_id=user_id,
            question=content,
            answer=response,
            session_id=session_id
        )
        
        return response
    
    def _get_or_create_user(self, wx_open_id: str) -> User:
        user = self.db.query(User).filter(User.wx_open_id == wx_open_id).first()
        if not user:
            user = User(wx_open_id=wx_open_id)
            self.db.add(user)
            self.db.commit()
        return user
    
    async def _get_context(self, user_id: str, current_query: str) -> List[dict]:
        # 获取相关的历史对话
        return await self.vector_service.search_similar_conversations(
            user_id=user_id,
            query=current_query,
            limit=5
        ) 