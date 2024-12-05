from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from models.chat_session import ChatSession
from models.message import Message
from datetime import datetime
import csv
import io
import json
from fastapi.responses import StreamingResponse

class ExportService:
    def __init__(self, db: Session):
        self.db = db
    
    async def export_sessions_to_csv(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> str:
        """导出会话数据到CSV"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 写入头部
        writer.writerow([
            "Session ID",
            "User ID",
            "Title",
            "Created At",
            "Updated At",
            "Message Count",
            "Is Active"
        ])
        
        # 查询会话
        query = self.db.query(ChatSession)
        if start_date:
            query = query.filter(ChatSession.created_at >= start_date)
        if end_date:
            query = query.filter(ChatSession.created_at <= end_date)
        
        sessions = query.all()
        
        # 写入数据
        for session in sessions:
            message_count = self.db.query(Message)\
                .filter(Message.session_id == session.session_id)\
                .count()
            
            writer.writerow([
                session.session_id,
                session.user_id,
                session.title,
                session.created_at.isoformat(),
                session.updated_at.isoformat(),
                message_count,
                session.is_active
            ])
        
        return output.getvalue()
    
    async def export_messages_to_json(
        self,
        session_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> str:
        """导出消息数据到JSON"""
        query = self.db.query(Message)
        
        if session_id:
            query = query.filter(Message.session_id == session_id)
        if start_date:
            query = query.filter(Message.created_at >= start_date)
        if end_date:
            query = query.filter(Message.created_at <= end_date)
        
        messages = query.order_by(Message.created_at).all()
        
        data = [
            {
                "message_id": msg.id,
                "session_id": msg.session_id,
                "user_id": msg.user_id,
                "content": msg.content,
                "message_type": msg.message_type,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
        
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    async def export_chat_history_csv(self, user_id: str) -> StreamingResponse:
        """导出聊天历史为CSV"""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["时间", "会话ID", "发送者", "内容"])
        
        messages = await self.db.query(Message)\
            .filter(Message.user_id == user_id)\
            .order_by(Message.created_at.desc())\
            .all()
            
        for msg in messages:
            writer.writerow([
                msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                msg.session_id,
                "用户" if msg.message_type == "user" else "AI",
                msg.content
            ])
        
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                'Content-Disposition': f'attachment; filename=chat_history_{datetime.now().strftime("%Y%m%d")}.csv'
            }
        ) 