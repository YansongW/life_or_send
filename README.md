# Life or Send - AI 客服系统

[![CI](https://github.com/yansongWang/life_or_send/actions/workflows/ci.yml/badge.svg)](https://github.com/yansongWang/life_or_send/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)

[中文](README.md) | [English](README_EN.md) | [한국어](README_KR.md)

## 项目概述
基于通义千问2-70B的智能客服系统，集成微信公众号平台。系统结合 RAG 技术提供准确的问题解答。

## 主要功能
- 微信公众号消息处理
- 多轮对话管理
- 基于RAG的知识检索
- 历史对话存储与搜索
- 会话管理与统计
- 管理员后台

## 技术栈
- **后端框架**: FastAPI
- **数据库**: 
  - MySQL (结构化数据)
  - Milvus (向量存储)
  - Redis (缓存)
- **AI模型**: Qwen2-70b (通过 Ollama 部署)
- **RAG框架**: RAGFlow

## 快速开始

### 环境要求
- Python 3.8+
- MySQL 8.0+
- Redis 6.0+
- Milvus 2.3+
- NVIDIA GPU (显存40GB以上)
- Docker & Docker Compose

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/yansongWang/life_or_send.git
cd life_or_send
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息
```

4. 启动服务
```bash
docker-compose up -d
```

5. 初始化数据库
```bash
python scripts/init_db.py
```

6. 启动服务器
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 文档
- [安装指南](INSTALL.md)
- [配置说明](CONFIG.md)
- [API文档](docs/api.md)
- [开发指南](docs/development.md)

## 贡献
请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目开发。

## 许可证
本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件
