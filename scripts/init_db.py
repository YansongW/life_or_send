import asyncio
import sys
from pathlib import Path
from alembic.config import Config
from alembic import command
from config.config import settings
import mysql.connector

async def init_database():
    """初始化数据库"""
    try:
        # 创建数据库
        conn = mysql.connector.connect(
            host=settings.DATABASE_URL.split("@")[1].split("/")[0],
            user=settings.DATABASE_URL.split("//")[1].split(":")[0],
            password=settings.DATABASE_URL.split(":")[2].split("@")[0]
        )
        cursor = conn.cursor()
        
        database = settings.DATABASE_URL.split("/")[-1]
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        
        # 运行迁移
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        
        print("✅ 数据库初始化完成")
        return True
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(init_database())
    sys.exit(0 if success else 1) 