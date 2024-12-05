import sys
import os
from pathlib import Path
from typing import List, Tuple
import importlib.util
import mysql.connector
import aioredis
import asyncio
from milvus import default_server
from milvus.grpc_gen.milvus_pb2 import Status

def check_python_version() -> Tuple[bool, str]:
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        return False, "Python版本必须 >= 3.8"
    return True, f"Python版本检查通过: {sys.version}"

def check_env_file() -> Tuple[bool, str]:
    """检查环境配置文件"""
    env_path = Path(".env")
    if not env_path.exists():
        return False, "未找到.env文件，请从.env.example复制并配置"
    return True, "环境配置文件检查通过"

async def check_database_connection() -> Tuple[bool, str]:
    """检查数据库连接"""
    try:
        from config.config import settings
        conn = mysql.connector.connect(
            host=settings.DATABASE_URL.split("@")[1].split("/")[0],
            user=settings.DATABASE_URL.split("//")[1].split(":")[0],
            password=settings.DATABASE_URL.split(":")[2].split("@")[0],
            database=settings.DATABASE_URL.split("/")[-1]
        )
        conn.close()
        return True, "数据库连接检查通过"
    except Exception as e:
        return False, f"数据库连接失败: {str(e)}"

async def check_redis_connection() -> Tuple[bool, str]:
    """检查Redis连接"""
    try:
        from config.config import settings
        redis = aioredis.from_url(settings.REDIS_URL)
        await redis.ping()
        await redis.close()
        return True, "Redis连接检查通过"
    except Exception as e:
        return False, f"Redis连接失败: {str(e)}"

async def check_milvus_connection() -> Tuple[bool, str]:
    """检查Milvus连接"""
    try:
        from config.config import settings
        connections.connect(
            host=settings.MILVUS_HOST,
            port=settings.MILVUS_PORT
        )
        return True, "Milvus连接检查通过"
    except Exception as e:
        return False, f"Milvus连接失败: {str(e)}"

async def check_ollama_connection() -> Tuple[bool, str]:
    """检查Ollama连接"""
    try:
        from config.config import settings
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.OLLAMA_API_URL}/api/tags")
            if response.status_code == 200:
                return True, "Ollama连接检查通过"
            return False, f"Ollama连接失败: {response.status_code}"
    except Exception as e:
        return False, f"Ollama连接失败: {str(e)}"

async def main():
    checks = [
        check_python_version(),
        check_env_file(),
        await check_database_connection(),
        await check_redis_connection(),
        await check_milvus_connection(),
        await check_ollama_connection()
    ]
    
    all_passed = True
    for success, message in checks:
        print(message)
        if not success:
            all_passed = False
    
    if not all_passed:
        print("\n❌ 系统检查未通过，请修复上述问题")
        sys.exit(1)
    print("\n✅ 所有系统检查通过")

if __name__ == "__main__":
    asyncio.run(main())