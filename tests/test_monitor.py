import pytest
from services.monitor_service import SystemMonitor

@pytest.mark.asyncio
async def test_check_system_resources():
    """Test system resource monitoring."""
    monitor = SystemMonitor()
    status = await monitor.check_system_resources()
    
    assert "cpu" in status
    assert "memory" in status
    assert "disk" in status
    
    assert isinstance(status["cpu"]["usage"], float)
    assert isinstance(status["memory"]["usage"], float)
    assert isinstance(status["disk"]["usage"], float)
    
    assert isinstance(status["cpu"]["alert"], bool)
    assert isinstance(status["memory"]["alert"], bool)
    assert isinstance(status["disk"]["alert"], bool) 