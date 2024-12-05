# AI客服机器人

## 项目概述
一个基于大语言模型的智能客服系统，集成微信公众号，提供自动化客户服务。系统使用本地部署的Qwen2-70b模型，结合RAG技术提供准确的问题解答。

### 主要功能
- 微信公众号消息处理
- 多轮对话管理
- 基于RAG的知识检索
- 历史对话存储与搜索
- 会话管理与统计
- 管理员后台

### 技术栈
- **后端框架**: FastAPI
- **数据库**:
  - MySQL (结构化数据)
  - Milvus (向量存储)
  - Redis (缓存)
- **AI模型**: Qwen2-70b (通过Ollama部署)
- **RAG框架**: RAGFlow

## 系统架构

### 核心组件
1. **API层**
   - 微信接口 (/api/wechat)
   - 聊天接口 (/api/chat)
   - 会话管理 (/api/sessions)
   - 搜索接口 (/api/search)
   - 统计分析 (/api/analytics)

2. **服务层**
   - 聊天服务 (ChatService)
   - AI服务 (AIService)
   - 向量服务 (VectorService)
   - 会话服务 (SessionService)
   - 微信服务 (WeChatService)

3. **数据层**
   - 用户信息
   - 消息记录
   - 会话管理
   - 向量存储
   - 缓存数据

### 数据流
1. 用户通过微信发送消息
2. 系统处理消息并检索相关上下文
3. AI模型结合RAG生成回复
4. 系统存储对话记录
5. 返回响应给用户

## 部署说明

### 环境要求
- Python 3.8+
- MySQL 8.0+
- Redis 6.0+
- Milvus 2.3+
- NVIDIA GPU (显存40GB以上)
- Docker & Docker Compose

### 快速开始
1. 克隆项目

```bash
git clone [项目地址]
cd [项目目录]
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息
```

4. 初始化数据库

```bash
alembic upgrade head
```

5. 启动服务

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 配置说明
详细配置说明请参考 [CONFIG.md](CONFIG.md)

## API文档
启动服务后访问 `/docs` 查看完整的API文档。

## 开发指南
1. 代码结构
```
chatbot/
├── api/          # API接口
├── models/       # 数据模型
├── services/     # 业务服务
├── database/     # 数据库配置
└── config/       # 系统配置
```

2. 主要模块
- 微信消息处理
- 对话管理
- 知识检索
- 数据分析

## 常见问题
1. 微信配置问题
2. 模型部署问题
3. 数据库连接问题
4. 性能优化建议

## 更新日志
- v1.0.0: 初始版本发布
- v1.1.0: 添加会话管理
- v1.2.0: 添加数据分析功能

## 贡献指南
欢迎提交 Issue 和 Pull Request

## 许可证
MIT License