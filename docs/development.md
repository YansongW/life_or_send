# Development Guide

## Project Structure

```
life_or_send/
├── api/                 # API endpoints
│   ├── wechat.py       # WeChat integration
│   ├── chat.py         # Chat management
│   └── analytics.py    # Analytics endpoints
├── services/           # Business logic
│   ├── chat_service.py
│   └── analytics_service.py
├── models/            # Database models
├── database/         # Database configuration
├── utils/            # Utility functions
├── tests/           # Test cases
└── scripts/         # Management scripts
```

## Development Setup

1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Set up pre-commit hooks
```bash
pre-commit install
```

## Database Migrations

Create new migration:
```bash
alembic revision -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

## Testing

Run tests:
```bash
pytest

# With coverage
pytest --cov=./ --cov-report=html
```

## Code Style

We use:
- black for code formatting
- isort for import sorting
- flake8 for linting

Format code:
```bash
black .
isort .
flake8
``` 