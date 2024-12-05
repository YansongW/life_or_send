import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import hashlib
from config.config import settings

def test_wechat_verification(client: TestClient):
    """Test WeChat server verification."""
    timestamp = str(int(datetime.now().timestamp()))
    nonce = "test_nonce"
    token = settings.WECHAT_TOKEN
    
    # Generate correct signature
    tmp_list = [token, timestamp, nonce]
    tmp_list.sort()
    tmp_str = "".join(tmp_list)
    signature = hashlib.sha1(tmp_str.encode()).hexdigest()
    
    response = client.get(
        "/api/v1/wechat",
        params={
            "signature": signature,
            "timestamp": timestamp,
            "nonce": nonce,
            "echostr": "test_echostr"
        }
    )
    
    assert response.status_code == 200
    assert response.text == "test_echostr"

def test_invalid_signature(client: TestClient):
    """Test invalid signature rejection."""
    response = client.get(
        "/api/v1/wechat",
        params={
            "signature": "invalid",
            "timestamp": "123",
            "nonce": "test",
            "echostr": "test"
        }
    )
    
    assert response.status_code == 403 