import pytest
from datetime import datetime, timedelta
from services.search_service import SearchService
from models.message import Message
from models.chat_session import ChatSession

@pytest.mark.asyncio
async def test_search_by_content(db_session):
    """Test message search by content."""
    # Create test data
    session = ChatSession(
        user_id="test_user",
        title="Test Session"
    )
    db_session.add(session)
    db_session.commit()
    
    message = Message(
        user_id="test_user",
        session_id=session.session_id,
        content="Test message content",
        message_type="user"
    )
    db_session.add(message)
    db_session.commit()
    
    service = SearchService(db_session)
    results = await service.search_by_content(
        user_id="test_user",
        keyword="test"
    )
    
    assert len(results) == 1
    assert results[0].content == "Test message content"

@pytest.mark.asyncio
async def test_get_session_statistics(db_session):
    """Test session statistics."""
    service = SearchService(db_session)
    stats = await service.get_session_statistics(
        user_id="test_user",
        start_date=datetime.utcnow() - timedelta(days=7)
    )
    
    assert isinstance(stats.total_sessions, int)
    assert isinstance(stats.total_messages, int)
    assert isinstance(stats.user_messages, int)
    assert isinstance(stats.bot_messages, int)
