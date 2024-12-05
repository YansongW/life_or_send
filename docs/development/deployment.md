# 部署指南

## 环境准备

### 系统要求
- Ubuntu 20.04 LTS
- Python 3.8+
- Docker & Docker Compose
- Nginx

### 安装基础软件

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装依赖
sudo apt install -y python3.8 python3.8-venv python3.8-dev
sudo apt install -y nginx docker.io docker-compose
```

## 部署步骤

### 1. 准备代码

```bash
# 克隆代码
git clone https://github.com/yansongWang/life_or_send.git
cd life_or_send

# 创建虚拟环境
python3.8 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件设置生产环境配置
```

### 3. 启动数据库服务

```bash
# 启动服务
docker-compose up -d mysql redis milvus

# 检查服务状态
docker-compose ps
```

### 4. 初始化数据库

```bash
# 运行数据库迁移
alembic upgrade head

# 初始化基础数据
python scripts/init_db.py
```

### 5. 配置 Nginx

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 6. 启动应用

```bash
# 使用 supervisord 管理进程
sudo apt install supervisor
sudo nano /etc/supervisor/conf.d/life_or_send.conf

[program:life_or_send]
command=/path/to/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
directory=/path/to/life_or_send
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/life_or_send.err.log
stdout_logfile=/var/log/life_or_send.out.log

# 重启 supervisor
sudo supervisorctl reread
sudo supervisorctl update
```

## 监控和维护

### 日志查看

```bash
# 应用日志
tail -f /var/log/life_or_send.out.log

# 错误日志
tail -f /var/log/life_or_send.err.log

# Nginx 日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 性能监控

```bash
# 系统资源
htop

# Docker 容器
docker stats

# 应用指标
curl http://localhost:8000/metrics
```

### 备份

```bash
# 数据库备份
python scripts/backup_db.py

# 文件备份
rsync -avz /path/to/life_or_send /backup/location
``` 