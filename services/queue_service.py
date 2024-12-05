import aio_pika
import json
import logging
from typing import Any, Dict
from config.config import settings
from services.retry_service import RetryService

logger = logging.getLogger(__name__)

class QueueService:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.retry_service = RetryService()
        
    async def connect(self):
        """连接到RabbitMQ"""
        if not self.connection:
            self.connection = await aio_pika.connect_robust(
                settings.RABBITMQ_URL
            )
            self.channel = await self.connection.channel()
            
            # 声明队列
            await self.channel.declare_queue(
                "chat_messages",
                durable=True
            )
    
    async def publish_message(
        self,
        queue_name: str,
        message: Dict[str, Any]
    ):
        """发布消息到队列（带重试）"""
        await self.retry_service.retry_async(
            self._publish_message,
            queue_name,
            message
        )
    
    async def _publish_message(
        self,
        queue_name: str,
        message: Dict[str, Any]
    ):
        """实际的消息发布逻辑"""
        try:
            await self.connect()
            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=queue_name
            )
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise
    
    async def consume_messages(
        self,
        queue_name: str,
        callback
    ):
        """消费队列消息"""
        try:
            await self.connect()
            queue = await self.channel.declare_queue(
                queue_name,
                durable=True
            )
            
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        await callback(json.loads(message.body.decode()))
        except Exception as e:
            logger.error(f"Failed to consume messages: {e}")
            raise
    
    async def close(self):
        """关闭连接"""
        if self.connection:
            await self.connection.close()
            self.connection = None
            self.channel = None 