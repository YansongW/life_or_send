import asyncio
import sys
import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
import hashlib
from config.config import settings
import pytest

async def test_wechat_interface():
    """测试微信接口"""
    base_url = "http://localhost:8000"  # 修改为您的服务器地址
    
    try:
        print("开始测试微信接口...\n")
        async with httpx.AsyncClient() as client:
            # 1. 测试服务器验证
            print("1. 测试服务器验证...")
            timestamp = str(int(datetime.now().timestamp()))
            nonce = "test_nonce"
            token = settings.WECHAT_TOKEN
            
            # 生成正确的签名
            tmp_list = [token, timestamp, nonce]
            tmp_list.sort()
            tmp_str = "".join(tmp_list)
            signature = hashlib.sha1(tmp_str.encode()).hexdigest()
            
            response = await client.get(
                f"{base_url}/wechat",
                params={
                    "signature": signature,
                    "timestamp": timestamp,
                    "nonce": nonce,
                    "echostr": "test_echostr"
                }
            )
            assert response.status_code == 200
            assert response.text == "test_echostr"
            print("✅ 服务器验证通过")
            
            # 2. 测试文本消息处理
            print("\n2. 测试文本消息处理...")
            test_xml = f"""
            <xml>
                <ToUserName><![CDATA[gh_test]]></ToUserName>
                <FromUserName><![CDATA[test_user]]></FromUserName>
                <CreateTime>{int(datetime.now().timestamp())}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[你好]]></Content>
                <MsgId>1234567890123456</MsgId>
            </xml>
            """
            
            response = await client.post(
                f"{base_url}/wechat",
                content=test_xml
            )
            assert response.status_code == 200
            
            # 解析响应XML
            xml_response = ET.fromstring(response.text)
            assert xml_response.find('ToUserName').text == 'test_user'
            assert xml_response.find('FromUserName').text == 'gh_test'
            assert xml_response.find('MsgType').text == 'text'
            print("✅ 文本消息处理正常")
            
            # 3. 测试事件消息处理
            print("\n3. 测试事件消息处理...")
            test_event_xml = f"""
            <xml>
                <ToUserName><![CDATA[gh_test]]></ToUserName>
                <FromUserName><![CDATA[test_user]]></FromUserName>
                <CreateTime>{int(datetime.now().timestamp())}</CreateTime>
                <MsgType><![CDATA[event]]></MsgType>
                <Event><![CDATA[subscribe]]></Event>
            </xml>
            """
            
            response = await client.post(
                f"{base_url}/wechat",
                content=test_event_xml
            )
            assert response.status_code == 200
            
            # 解析响应XML
            xml_response = ET.fromstring(response.text)
            assert xml_response.find('MsgType').text == 'text'
            print("✅ 事件消息处理正常")
            
            print("\n✅ 所有测试通过")
            return True
            
    except AssertionError as e:
        print(f"\n❌ 测试断言失败: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ 测试异常: {str(e)}")
        return False

@pytest.mark.asyncio
async def test_invalid_signature():
    """测试无效签名"""
    base_url = "http://localhost:8000"  # 修改为您的服务器地址
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/wechat",
            params={
                "signature": "invalid",
                "timestamp": "123",
                "nonce": "test",
                "echostr": "test"
            }
        )
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_message_handling():
    """Test message handling."""
    base_url = "http://localhost:8000"
    async with httpx.AsyncClient() as client:
        # Test text message
        test_xml = f"""
        <xml>
            <ToUserName><![CDATA[gh_test]]></ToUserName>
            <FromUserName><![CDATA[test_user]]></FromUserName>
            <CreateTime>{int(datetime.now().timestamp())}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[测试消息]]></Content>
            <MsgId>1234567890123456</MsgId>
        </xml>
        """
        
        response = await client.post(
            f"{base_url}/wechat",
            content=test_xml
        )
        assert response.status_code == 200
        
        # Test event message
        test_event_xml = f"""
        <xml>
            <ToUserName><![CDATA[gh_test]]></ToUserName>
            <FromUserName><![CDATA[test_user]]></FromUserName>
            <CreateTime>{int(datetime.now().timestamp())}</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[subscribe]]></Event>
        </xml>
        """
        
        response = await client.post(
            f"{base_url}/wechat",
            content=test_event_xml
        )
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_invalid_xml():
    """Test invalid XML handling."""
    base_url = "http://localhost:8000"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/wechat",
            content="invalid xml"
        )
        assert response.status_code == 200  # Should return error message

if __name__ == "__main__":
    success = asyncio.run(test_wechat_interface())
    sys.exit(0 if success else 1) 