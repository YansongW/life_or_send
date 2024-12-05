# 配置说明文档

本文档详细说明了系统运行所需的所有配置项。请在部署前正确配置这些参数。

## 必需配置项

### 数据库配置
- `DATABASE_URL`: MySQL数据库连接URL
  - 格式：`mysql://用户名:密码@主机:端口/数据库名`
  - 示例：`mysql://chatbot:password123@localhost:3306/chatbot`

### 微信配置
- `WECHAT_APP_ID`: 微信公众号的AppID
  - 获取位置：微信公众平台 -> 开发 -> 基本配置
  - 示例：`wx1234567890abcdef`

- `WECHAT_APP_SECRET`: 微信公众号的AppSecret
  - 获取位置：微信公众平台 -> 开发 -> 基本配置
  - 示例：`1234567890abcdef1234567890abcdef`

- `WECHAT_TOKEN`: 微信公众号的Token
  - 获取位置：微信公众平台 -> 开发 -> 基本配置
  - 自定义设置，用于验证消息来源

### Ollama配置
- `OLLAMA_API_URL`: Ollama服务的API地址
  - 默认值：`http://localhost:11434`
  - 如果部署在其他服务器，请修改为对应地址

- `MODEL_NAME`: 使用的模型名称
  - 默认值：`qwen2-70b`
  - 可选值：根据您的Ollama安装的模型而定

### Milvus配置
- `MILVUS_HOST`: Milvus服务器地址
  - 默认值：`localhost`
  - 如果部署在其他服务器，请修改为对应地址

- `MILVUS_PORT`: Milvus服务端口
  - 默认值：`19530`

- `MILVUS_COLLECTION`: Milvus集合名称
  - 默认值：`chat_history`
  - 可自定义，用于存储向量数据

## 可选配置项

### 系统配置
- `LOG_LEVEL`: 日志级别
  - 默认值：`INFO`
  - 可选值：`DEBUG`, `INFO`, `WARNING`, `ERROR`

- `MAX_SESSIONS_PER_USER`: 每个用户最大会话数
  - 默认值：`10`
  - 建议范围：5-20

- `MAX_MESSAGES_PER_SESSION`: 每个会话最大消息数
  - 默认值：`100`
  - 建议范围：50-200

- `CONTEXT_WINDOW_SIZE`: 上下文窗口大小
  - 默认值：`20`
  - 建议范围：10-30

## 配置步骤

1. 复制环境变量模板文件：