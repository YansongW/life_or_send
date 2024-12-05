import asyncio
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config.config import settings
from models.user import User, UserRole
from models.chat_session import ChatSession
from models.message import Message

async def test_database():
    """测试数据库功能"""
    try:
        # 1. 测试数据库连接
        engine = create_engine(settings.DATABASE_URL)
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        print("1. 测试数据库连接...")
        result = db.execute(text("SELECT 1"))
        assert result.scalar() == 1
        print("✅ 数据库连接成功")

        # 2. 测试用户表
        print("\n2. 测试用户表...")
        test_user = User(
            wx_open_id="test_user_001",
            nickname="测试用户",
            role=UserRole.USER
        )
        db.add(test_user)
        db.commit()
        
        queried_user = db.query(User).filter_by(wx_open_id="test_user_001").first()
        assert queried_user is not None
        assert queried_user.nickname == "测试用户"
        print("✅ 用户表操作正常")

        # 3. 测试会话表
        print("\n3. 测试会话表...")
        test_session = ChatSession(
            user_id=test_user.wx_open_id,
            title="测试会话",
            context="[]"
        )
        db.add(test_session)
        db.commit()
        
        queried_session = db.query(ChatSession).filter_by(user_id=test_user.wx_open_id).first()
        assert queried_session is not None
        assert queried_session.title == "测试会话"
        print("✅ 会话表操作正常")

        # 4. 测试消息表
        print("\n4. 测试消息表...")
        test_message = Message(
            user_id=test_user.wx_open_id,
            session_id=queried_session.session_id,
            content="测试消息",
            message_type="user"
        )
        db.add(test_message)
        db.commit()
        
        queried_message = db.query(Message).filter_by(session_id=queried_session.session_id).first()
        assert queried_message is not None
        assert queried_message.content == "测试消息"
        print("✅ 消息表操作正常")

        # 5. 测试关联查询
        print("\n5. 测试关联查询...")
        session_with_messages = db.query(ChatSession)\
            .filter_by(user_id=test_user.wx_open_id)\
            .first()
        messages = db.query(Message)\
            .filter_by(session_id=session_with_messages.session_id)\
            .all()
        assert len(messages) > 0
        print("✅ 关联查询正常")

        # 清理测试数据
        print("\n6. 清理测试数据...")
        db.query(Message).filter_by(session_id=queried_session.session_id).delete()
        db.query(ChatSession).filter_by(user_id=test_user.wx_open_id).delete()
        db.query(User).filter_by(wx_open_id="test_user_001").delete()
        db.commit()
        print("✅ 测试数据清理完成")

        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("开始数据库功能测试...\n")
    success = asyncio.run(test_database())
    if success:
        print("\n✅ 所有测试通过")
        sys.exit(0)
    else:
        print("\n❌ 测试失败")
        sys.exit(1) 