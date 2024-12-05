# API 概述

## 认证方式

所有API请求需要在Header中携带Token：

```http
Authorization: Bearer <your_token>
```

## 响应格式

所有API响应都遵循以下格式：

```json
{
    "success": true,
    "data": {
        // 响应数据
    },
    "error": null,
    "timestamp": "2024-01-01T12:00:00Z"
}
```

错误响应格式：

```json
{
    "success": false,
    "data": null,
    "error": {
        "code": 5001,
        "message": "操作失败",
        "detail": "详细错误信息"
    },
    "timestamp": "2024-01-01T12:00:00Z"
}
```

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 4001 | 会话创建失败 |
| 4002 | 获取会话失败 |
| 5001 | 搜索失败 |
| 6001 | 统计失败 |
| 7001 | 系统监控失败 |
| 8001 | 数据导出失败 |

## 分页参数

支持分页的接口都接受以下参数：

- `page`: 页码，从1开始
- `page_size`: 每页数量，默认20 