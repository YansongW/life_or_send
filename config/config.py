from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import validator

class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "mysql://user:password@your-cloud-host/chatbot"
    
    # 微信配置
    WECHAT_APP_ID: str
    WECHAT_APP_SECRET: str
    WECHAT_TOKEN: str
    WECHAT_ENCODING_AES_KEY: Optional[str] = None  # 如果需要加密模式
    WECHAT_MESSAGE_TIMEOUT: int = 4500  # 消息处理超时时间（毫秒）
    
    # Ollama配置
    OLLAMA_API_URL: str = "http://localhost:11434"
    MODEL_NAME: str = "qwen2-70b"
    
    # RAGFlow配置
    RAGFLOW_CONFIG = {
        "embedding_model": "text2vec-base",
        "vector_store": {
            "type": "milvus",
            "host": "your-cloud-host",
            "port": 19530,
            "collection_name": "chat_history"
        },
        "chunk_size": 500,
        "chunk_overlap": 50
    }

    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not v.startswith(("mysql://", "postgresql://")):
            raise ValueError("Invalid database URL")
        return v
    
    @validator("RABBITMQ_URL")
    def validate_rabbitmq_url(cls, v):
        if not v.startswith("amqp://"):
            raise ValueError("Invalid RabbitMQ URL")
        return v
    
    class Config:
        env_file = ".env"

settings = Settings() 