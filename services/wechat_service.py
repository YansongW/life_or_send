from typing import Optional
import httpx
from config import settings
import logging

logger = logging.getLogger(__name__)

class WeChatService:
    def __init__(self):
        self.access_token: Optional[str] = None
    
    async def get_access_token(self) -> str:
        """获取微信访问令牌"""
        if not self.access_token:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.weixin.qq.com/cgi-bin/token",
                    params={
                        "grant_type": "client_credential",
                        "appid": settings.WECHAT_APP_ID,
                        "secret": settings.WECHAT_APP_SECRET
                    }
                )
                data = response.json()
                if "access_token" in data:
                    self.access_token = data["access_token"]
                else:
                    raise ValueError(f"Failed to get access token: {data}")
        return self.access_token
    
    async def send_customer_message(
        self,
        user_openid: str,
        content: str
    ) -> bool:
        """发送客服消息"""
        try:
            access_token = await self.get_access_token()
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://api.weixin.qq.com/cgi-bin/message/custom/send",
                    params={"access_token": access_token},
                    json={
                        "touser": user_openid,
                        "msgtype": "text",
                        "text": {
                            "content": content
                        }
                    }
                )
                return response.json().get("errcode") == 0
        except Exception as e:
            logger.error(f"Failed to send customer message: {e}")
            return False 