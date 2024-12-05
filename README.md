# Life or Send - AI Customer Service System

[![CI](https://github.com/yansongWang/life_or_send/actions/workflows/ci.yml/badge.svg)](https://github.com/yansongWang/life_or_send/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)

[中文文档](README_ZH.md)

## Overview
An intelligent customer service system powered by Qwen2-70b, integrated with WeChat Official Account platform. The system combines RAG technology to provide accurate responses.

## Features
- WeChat message handling
- Multi-turn conversation management
- RAG-based knowledge retrieval
- Chat history storage and search
- Session management and analytics
- Admin dashboard

## Tech Stack
- **Backend**: FastAPI
- **Databases**: 
  - MySQL (structured data)
  - Milvus (vector storage)
  - Redis (cache)
- **AI Model**: Qwen2-70b (via Ollama)
- **RAG Framework**: RAGFlow

## Quick Start
1. Clone the repository
```bash
git clone https://github.com/yansongWang/life_or_send.git
cd life_or_send
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure environment
```bash
cp .env.example .env
# Edit .env with your configurations
```

4. Initialize database
```bash
python scripts/init_db.py
```

5. Start server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Documentation
- [Installation Guide](INSTALL.md)
- [Configuration Guide](CONFIG.md)
- [API Documentation](docs/api.md)
- [Development Guide](docs/development.md)

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.# life_or_send
