from fastapi import APIRouter, Request, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from services.chat_service import ChatService
from database.db import get_db
import xml.etree.ElementTree as ET
from datetime import datetime
import hashlib
import time
from config import settings
import logging
import asyncio
import uuid

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/wechat")
async def verify_wechat(signature: str, timestamp: str, nonce: str, echostr: str):
    """微信服务器验证接口"""
    token = settings.WECHAT_TOKEN  # 应该从配置中获取，而不是硬编码
    tmp_list = [token, timestamp, nonce]
    tmp_list.sort()
    tmp_str = "".join(tmp_list)
    
    if hashlib.sha1(tmp_str.encode()).hexdigest() == signature:
        return echostr
    raise HTTPException(status_code=403, detail="Invalid signature")

@router.post("/wechat")
async def handle_wechat_message(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """处理微信消息"""
    request_id = str(uuid.uuid4())
    logger.info(f"Request {request_id}: Received WeChat message")
    try:
        body = await request.body()
        if not body:
            logger.error(f"Request {request_id}: Empty request body")
            return create_reply("系统错误", "system", "user")
        
        xml_data = ET.fromstring(body)
        if xml_data is None:
            logger.error(f"Request {request_id}: Invalid XML format")
            return create_reply("消息格式错误", "system", "user")
    except Exception as e:
        logger.error(f"Failed to parse XML: {e}")
        return create_reply("系统错误，请稍后重试", "from_user", "to_user")

    try:
        msg_type = xml_data.find('MsgType').text
        from_user = xml_data.find('FromUserName').text
        to_user = xml_data.find('ToUserName').text
    except AttributeError as e:
        logger.error(f"Missing required XML fields: {e}")
        return create_reply("消息格式错误", from_user, to_user)
    
    chat_service = ChatService(db)
    
    # 处理不同类型的消息
    if msg_type == 'text':
        try:
            content = xml_data.find('Content').text
            async with asyncio.timeout(4.5):  # 留0.5秒的缓冲时间
                response = await chat_service.handle_message(from_user, content)
                return create_reply(to_user, from_user, response)
        except asyncio.TimeoutError:
            # 如果处理超时，返回提示消息，并在后台继续处理
            background_tasks.add_task(
                handle_message_background,
                chat_service,
                from_user,
                content
            )
            return create_reply(
                to_user,
                from_user,
                "您的问题正在处理中，稍后会通过客服消息回复您。"
            )
    elif msg_type == 'event':
        return await handle_event_message(xml_data, chat_service)
    elif msg_type == 'image':
        return await handle_image_message(xml_data, chat_service)
    
    # 默认回复
    return create_reply(
        to_user,
        from_user,
        "抱歉，暂时无法处理该类型的消息。"
    )

async def handle_event_message(xml_data: ET.Element, chat_service: ChatService):
    """处理事件消息"""
    event_type = xml_data.find('Event').text
    from_user = xml_data.find('FromUserName').text
    
    if event_type.lower() == 'subscribe':
        # 处理订阅事件
        welcome_msg = "欢迎关注！我是您的智能客服助手。请问有什么可以帮您的吗？"
        return create_reply(from_user, xml_data.find('ToUserName').text, welcome_msg)
    
    return None

async def handle_image_message(xml_data: ET.Element, chat_service: ChatService):
    """处理图片消息"""
    from_user = xml_data.find('FromUserName').text
    pic_url = xml_data.find('PicUrl').text
    
    response = "抱歉，暂时无法处理图片消息。请用文字描述您的问题。"
    return create_reply(from_user, xml_data.find('ToUserName').text, response)

def create_reply(to_user: str, from_user: str, content: str):
    """创建回复消息"""
    from fastapi.responses import XMLResponse
    
    xml_content = f"""
    <xml>
        <ToUserName><![CDATA[{to_user}]]></ToUserName>
        <FromUserName><![CDATA[{from_user}]]></FromUserName>
        <CreateTime>{int(time.time())}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{content}]]></Content>
    </xml>
    """
    return XMLResponse(content=xml_content) 

# 添加后台处理函数
async def handle_message_background(
    chat_service: ChatService,
    user_id: str,
    content: str
):
    """后台处理消息"""
    try:
        # 调用AI服务获取回复
        response = await chat_service.handle_message(user_id, content)
        
        # 通过客服消息发送回复
        wechat_service = WeChatService()
        await wechat_service.send_customer_message(user_id, response)
    except Exception as e:
        logger.error(f"Background message handling failed: {e}") 