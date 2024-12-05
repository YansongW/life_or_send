import pytest
from datetime import datetime
from models.chat_session import ChatSession
from services.session_service import SessionService

@pytest.mark.asyncio
async def test_create_session(db_session):
    """Test session creation."""
    service = SessionService(db_session)
    user_id = "test_user"
    title = "Test Session"
    
    session = await service.create_session(user_id, title)
    assert session.user_id == user_id
    assert session.title == title
    assert session.is_active == True

@pytest.mark.asyncio
async def test_get_user_sessions(db_session):
    """Test getting user sessions."""
    service = SessionService(db_session)
    user_id = "test_user"
    
    # Create test sessions
    await service.create_session(user_id, "Session 1")
    await service.create_session(user_id, "Session 2")
    
    sessions = await service.get_user_sessions(user_id)
    assert len(sessions) == 2
    assert all(s.user_id == user_id for s in sessions)

@pytest.mark.asyncio
async def test_update_context(db_session):
    """Test context update."""
    service = SessionService(db_session)
    session = await service.create_session("test_user", "Test Session")
    
    user_msg = "Hello"
    bot_msg = "Hi there"
    updated_session = await service.update_context(
        session.session_id,
        user_msg,
        bot_msg
    )
    
    context = updated_session.get_context()
    assert len(context) == 2
    assert context[0]["role"] == "user"
    assert context[0]["content"] == user_msg 