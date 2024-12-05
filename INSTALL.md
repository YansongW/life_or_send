# Installation Guide

## System Requirements

### Hardware Requirements
- CPU: 8+ cores
- Memory: 32GB+
- GPU: NVIDIA GPU with 40GB+ VRAM (for Qwen2-70b)
- Storage: 100GB+ available space

### Software Requirements
- Ubuntu 20.04 LTS or higher
- Python 3.8+
- MySQL 8.0+
- Redis 6.0+
- Milvus 2.3+
- Docker & Docker Compose

## Installation Steps

### 1. System Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3.8 python3.8-venv python3.8-dev
sudo apt install -y mysql-server redis-server
sudo apt install -y docker.io docker-compose
```

### 2. Database Setup
```bash
# MySQL
sudo mysql_secure_installation
sudo mysql -u root -p
CREATE DATABASE chatbot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'chatbot'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON chatbot.* TO 'chatbot'@'localhost';
FLUSH PRIVILEGES;

# Redis
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

## 基础环境安装

### 1. Python环境 