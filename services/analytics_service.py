from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models.chat_session import ChatSession
from models.message import Message
from models.user import User
from datetime import datetime, timedelta

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_daily_usage_stats(
        self,
        days: int = 30
    ) -> List[Dict]:
        """获取每日使用统计"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # 按日统计消息数量
        daily_stats = self.db.query(
            func.date(Message.created_at).label('date'),
            func.count(Message.id).label('total_messages'),
            func.count(Message.id).filter(Message.message_type == 'user').label('user_messages'),
            func.count(Message.id).filter(Message.message_type == 'bot').label('bot_messages')
        ).filter(
            Message.created_at >= start_date
        ).group_by(
            func.date(Message.created_at)
        ).all()
        
        return [
            {
                "date": str(stat.date),
                "total_messages": stat.total_messages,
                "user_messages": stat.user_messages,
                "bot_messages": stat.bot_messages
            }
            for stat in daily_stats
        ]
    
    async def get_user_activity_stats(self) -> List[Dict]:
        """获取用户活跃度统计"""
        # 统计每个用户的会话和消息数量
        user_stats = self.db.query(
            User.wx_open_id,
            User.nickname,
            func.count(distinct(ChatSession.id)).label('total_sessions'),
            func.count(Message.id).label('total_messages')
        ).join(
            ChatSession, User.wx_open_id == ChatSession.user_id
        ).join(
            Message, ChatSession.session_id == Message.session_id
        ).group_by(
            User.wx_open_id
        ).all()
        
        return [
            {
                "user_id": stat.wx_open_id,
                "nickname": stat.nickname,
                "total_sessions": stat.total_sessions,
                "total_messages": stat.total_messages
            }
            for stat in user_stats
        ]
    
    async def get_response_time_stats(self) -> Dict:
        """获取响应时间统计"""
        # 计算平均响应时间
        response_times = []
        messages = self.db.query(Message).order_by(
            Message.session_id, Message.created_at
        ).all()
        
        for i in range(1, len(messages)):
            if (messages[i].message_type == 'bot' and 
                messages[i-1].message_type == 'user' and
                messages[i].session_id == messages[i-1].session_id):
                response_time = (messages[i].created_at - messages[i-1].created_at).total_seconds()
                response_times.append(response_time)
        
        if response_times:
            return {
                "average_response_time": sum(response_times) / len(response_times),
                "min_response_time": min(response_times),
                "max_response_time": max(response_times)
            }
        return {
            "average_response_time": 0,
            "min_response_time": 0,
            "max_response_time": 0
        }
    
    async def get_topic_distribution(self) -> List[Dict]:
        """获取会话主题分布"""
        topic_stats = self.db.query(
            ChatSession.title,
            func.count(ChatSession.id).label('count')
        ).group_by(
            ChatSession.title
        ).all()
        
        return [
            {
                "topic": stat.title,
                "count": stat.count
            }
            for stat in topic_stats
        ]
    
    async def get_user_behavior_stats(self, user_id: str) -> Dict:
        """获取用户行为统计"""
        # 基础统计
        basic_stats = await self.db.query(
            func.count(Message.id).label('total_messages'),
            func.count(distinct(ChatSession.id)).label('total_sessions'),
            func.avg(func.length(Message.content)).label('avg_message_length')
        ).join(ChatSession)\
        .filter(Message.user_id == user_id)\
        .first()
        
        # 活跃时间分布
        hour_distribution = await self.db.query(
            func.extract('hour', Message.created_at).label('hour'),
            func.count(Message.id).label('count')
        ).filter(Message.user_id == user_id)\
        .group_by('hour')\
        .all()
        
        return {
            "basic_stats": {
                "total_messages": basic_stats.total_messages,
                "total_sessions": basic_stats.total_sessions,
                "avg_message_length": round(basic_stats.avg_message_length, 2)
            },
            "hour_distribution": {
                str(h.hour): h.count for h in hour_distribution
            }
        }