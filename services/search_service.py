from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from models.chat_session import ChatSession
from models.message import Message
from datetime import datetime

class SearchService:
    def __init__(self, db: Session):
        self.db = db
    
    async def search_by_content(
        self,
        user_id: Optional[str],
        keyword: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[Dict]:
        """搜索消息内容"""
        query = self.db.query(Message)\
            .join(ChatSession)\
            .filter(ChatSession.is_active == True)
        
        if user_id:
            query = query.filter(Message.user_id == user_id)
        
        if keyword:
            query = query.filter(Message.content.contains(keyword))
        
        messages = query.order_by(Message.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
        
        return [
            {
                "message_id": msg.id,
                "session_id": msg.session_id,
                "content": msg.content,
                "message_type": msg.message_type,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    
    async def get_session_statistics(
        self,
        user_id: Optional[str],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """获取会话统计信息"""
        query = self.db.query(ChatSession)\
            .filter(ChatSession.is_active == True)
        
        if user_id:
            query = query.filter(ChatSession.user_id == user_id)
        
        if start_date:
            query = query.filter(ChatSession.created_at >= start_date)
        if end_date:
            query = query.filter(ChatSession.created_at <= end_date)
        
        total_sessions = query.count()
        
        # 获取消息统计
        message_query = self.db.query(Message)\
            .join(ChatSession)\
            .filter(ChatSession.is_active == True)
        
        if user_id:
            message_query = message_query.filter(Message.user_id == user_id)
        
        total_messages = message_query.count()
        user_messages = message_query.filter(Message.message_type == 'user').count()
        bot_messages = message_query.filter(Message.message_type == 'bot').count()
        
        return {
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "user_messages": user_messages,
            "bot_messages": bot_messages,
            "average_messages_per_session": total_messages / total_sessions if total_sessions > 0 else 0
        } 