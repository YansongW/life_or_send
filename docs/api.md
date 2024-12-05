# API Documentation

## Authentication

All API endpoints require authentication unless specified otherwise.

### Headers
```
Authorization: Bearer <token>
```

## Endpoints

### WeChat Integration

#### GET /api/v1/wechat
WeChat server verification endpoint.

Parameters:
- `signature`: Signature from WeChat
- `timestamp`: Timestamp
- `nonce`: Nonce string
- `echostr`: Echo string

#### POST /api/v1/wechat
Handle WeChat messages.

Request Body: XML format from WeChat

### Chat Management

#### GET /api/v1/chat/history
Get chat history.

Parameters:
- `session_id`: Session ID
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

#### POST /api/v1/chat/send
Send message.

Request Body:
```json
{
    "content": "message content",
    "session_id": "optional session id"
}
```

### Analytics

#### GET /api/v1/analytics/daily-usage
Get daily usage statistics.

Parameters:
- `days`: Number of days (default: 30)

Response:
```json
{
    "success": true,
    "data": [
        {
            "date": "2024-01-01",
            "total_messages": 100,
            "user_messages": 50,
            "bot_messages": 50
        }
    ]
}
``` 