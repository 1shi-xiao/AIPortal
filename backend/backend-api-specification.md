# AI门户系统后端接口规范

## 项目概述
基于Vue 3的AI门户系统后端接口设计，包含用户管理、AI工具、文件管理、聊天功能、数据统计等模块。

## 技术规范
- **协议**: HTTP/HTTPS
- **数据格式**: JSON
- **认证方式**: JWT Token
- **API前缀**: `/api/v1`
- **状态码**: RESTful标准

## 接口目录
1. [用户认证接口](#1-用户认证接口)
2. [AI工具管理接口](#2-ai工具管理接口)
3. [文件管理接口](#3-文件管理接口)
4. [AI聊天接口](#4-ai聊天接口)
5. [数据统计接口](#5-数据统计接口)
6. [系统设置接口](#6-系统设置接口)
7. [搜索接口](#7-搜索接口)

---

## 1. 用户认证接口

### 1.1 用户注册
**POST** `/api/v1/auth/register`

**请求参数**:
```json
{
  "username": "string",      // 用户名(必填)
  "email": "string",         // 邮箱(必填)
  "password": "string",      // 密码(必填)
  "phone": "string",         // 手机号(可选)
  "company": "string"        // 公司(可选)
}
```

**响应参数**:
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "userId": "123456",
    "username": "user123",
    "email": "user@example.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### 1.2 用户登录
**POST** `/api/v1/auth/login`

**请求参数**:
```json
{
  "username": "string",      // 用户名或邮箱(必填)
  "password": "string"        // 密码(必填)
}
```

**响应参数**:
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "userId": "123456",
    "username": "user123",
    "email": "user@example.com",
    "avatar": "https://example.com/avatar.jpg",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 86400
  }
}
```

### 1.3 获取用户信息
**GET** `/api/v1/auth/userinfo`

**请求头**:
```
Authorization: Bearer {token}
```

**响应参数**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "userId": "123456",
    "username": "user123",
    "email": "user@example.com",
    "phone": "13800138000",
    "avatar": "https://example.com/avatar.jpg",
    "company": "示例公司",
    "role": "user",
    "createdAt": "2023-01-01T00:00:00Z",
    "lastLoginAt": "2023-10-15T14:30:00Z"
  }
}
```

### 1.4 更新用户信息
**PUT** `/api/v1/auth/userinfo`

**请求头**:
```
Authorization: Bearer {token}
```

**请求参数**:
```json
{
  "username": "string",      // 用户名(可选)
  "phone": "string",          // 手机号(可选)
  "company": "string",        // 公司(可选)
  "avatar": "string"         // 头像URL(可选)
}
```

**响应参数**:
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "userId": "123456",
    "username": "newusername",
    "phone": "13900139000",
    "company": "新公司",
    "avatar": "https://example.com/newavatar.jpg"
  }
}
```

### 1.5 修改密码
**PUT** `/api/v1/auth/password`

**请求头**:
```
Authorization: Bearer {token}
```

**请求参数**:
```json
{
  "oldPassword": "string",   // 旧密码(必填)
  "newPassword": "string"    // 新密码(必填)
}
```

**响应参数**:
```json
{
  "code": 200,
  "message": "密码修改成功"
}
```

### 1.6 刷新Token
**POST** `/api/v1/auth/refresh`

**请求头**:
```
Authorization: Bearer {refresh_token}
```

**响应参数**:
```json
{
  "code": 200,
  "message": "Token刷新成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 86400
  }
}
```

---

## 2. AI工具管理接口

### 2.1 获取AI工具列表
**GET** `/api/v1/ai-tools`

**查询参数**:
```
?category=string&page=1&limit=10&sort=created_at&order=desc
```

**响应参数**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "total": 50,
    "page": 1,
    "limit": 10,
    "list": [
      {
        "toolId": "tool_001",
        "name": "合同审查助手",
        "category": "management",
        "description": "智能合同审查与风险评估",
        "icon": "📝",
        "status": "active",
        "usageCount": 1234,
        "rating": 4.5,
        "createdAt": "2023-01-01T00:00:00Z",
        "lastUsedAt": "2023-10-15T14:30:00Z"
      }
    ]
  }
}
```

### 2.2 获取工具详情
**GET** `/api/v1/ai-tools/{toolId}`

**响应参数**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "toolId": "tool_001",
    "name": "合同审查助手",
    "category": "management",
    "description": "智能合同审查与风险评估",
    "detailedDescription": "合同审查助手是一款基于人工智能技术的合同分析工具...",
    "icon": "📝",
    "features": [
      "自动识别合同中的关键条款和风险点",
      "提供合同合规性评估和建议",
      "支持多种合同类型的智能审查"
    ],
    "example": "上传合同文档 → AI自动分析 → 查看风险报告 → 接收改进建议",
    "status": "active",
    "usageCount": 1234,
    "rating": 4.5,
    "config": {
      "maxFileSize": 10485760,
      "supportedFormats": ["pdf", "doc", "docx"],
      "processingTime": "2-5分钟"
    },
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-10-01T00:00:00Z"
  }
}
```

### 2.3 使用AI工具
**POST** `/api/v1/ai-tools/{toolId}/use`

**请求头**:
```
Authorization: Bearer {token}
```

**请求参数**:
```json
{
  "input": "string",           // 输入内容
  "parameters": {             // 工具特定参数
    "model": "default",
    "temperature": 0.7
  }
}
```

**响应参数**:
```json
{
  "code": 200,
  "message": "处理成功",
  "data": {
    "taskId": "task_123456",
    "result": "分析结果内容...",
    "status": "completed",
    "processingTime": 2.5,
    "confidence": 0.95,
    "createdAt": "2023-10-15T14:30:00Z"
  }
}
```

### 2.4 获取工具使用记录
**GET** `/api/v1/ai-tools/usage-history`

**请求头**:
```
Authorization: Bearer {token}
```

**查询参数**:
```
?toolId=string&startDate=2023-01-01&endDate=2023-12-31&page=1&limit=20
```

**响应参数**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "total": 100,
    "page": 1,
    "limit": 20,
    "list": [
      {
        "usageId": "usage_001",
        "toolId": "tool_001",
        "toolName": "合同审查助手",
        "input": "合同内容...",
        "result": "分析结果...",
        "status": "completed",
        "processingTime": 2.5,
        "createdAt": "2023-10-15T14:30:00Z"
      }
    ]
  }
}
```

### 2.5 获取热门工具
**GET** `/api/v1/ai-tools/hot`

**查询参数**:
```
?limit=10&timeRange=7d  // 7d, 30d, 90d
```

**响应参数**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": [
    {
      "toolId": "tool_001",
      "name": "合同审查助手",
      "icon": "📝",
      "usageCount": 1234,
      "rating": 4.5,
      "trend": "up"  // up, down, stable
    }
  ]
}
```

---

## 3. 文件管理接口

### 3.1 上传文件
**POST** `/api/v1/files/upload`

**请求头**:
```
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**请求参数**:
```
file: File          // 文件
folder: string      // 目标文件夹(可选)
tags: string[]     // 标签(可选)
```

**响应参数**:
```json
{
  "code": 200,
  "message": "上传成功",
  "data": {
    "fileId": "file_123456",
    "filename": "document.pdf",
    "originalName": "项目文档.pdf",
    "fileSize": 2345678,
    "mimeType": "application/pdf",
    "folder": "/documents",
    "tags": ["合同", "项目"],
    "uploadUrl": "https://storage.example.com/files/file_123456.pdf",
    "downloadUrl": "https://api.example.com/api/v1/files/file_123456/download",
    "createdAt": "2023-10-15T14:30:00Z"
  }
}
```

### 3.2 获取文件列表
**GET** `/api/v1/files`

**请求头**:
```
Authorization: Bearer {token}
```

**查询参数**:
```
?folder=string&page=1&limit=20&sort=created_at&order=desc&search=keyword
```

**响应参数**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "total": 50,
    "page": 1,
    "limit": 20,
    "list": [
      {
        "fileId": "file_123456",
        "filename": "document.pdf",
        "originalName": "项目文档.pdf",
        "fileSize": 2345678,
        "mimeType": "application/pdf",
        "icon": "📄",
        "folder": "/documents",
        "tags": ["合同", "项目"],
        "downloadUrl": "https://api.example.com/api/v1/files/file_123456/download",
        "createdAt": "2023-10-15T14:30:00Z",
        "updatedAt": "2023-10-15T14:30:00Z"
      }
    ]
  }
}
```

### 3.3 下载文件
**GET** `/api/v1/files/{fileId}/download`

**请求头**:
```
Authorization: Bearer {token}
```

**响应**: 文件流

### 3.4 删除文件
**DELETE** `/api/v1/files/{fileId}`

**请求头**:
```
Authorization: Bearer {token}
```

**响应参数**:
```json
{
  "code": 200,
  "message": "删除成功"
}
```

### 3.5 更新文件信息
**PUT** `/api/v1/files/{fileId}`

**请求头**:
```
Authorization: Bearer {token}
```

**请求参数**:
```json
{
  "filename": "string",      // 新文件名(可选)
  "folder": "string",        // 文件夹(可选)
  "tags": ["string"]         // 标签(可选)
}
```

**响应参数**:
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "fileId": "file_123456",
    "filename": "new_document.pdf",
    "folder": "/new_folder",
    "tags": ["合同", "项目", "重要"]
  }
}
```

---

## 4. AI聊天接口

### 4.1 创建聊天会话
**POST** `/api/v1/chat/sessions`

**请求头**:
```
Authorization: Bearer {token}
```

**请求参数**:
```json
{
  "title": "string",         // 会话标题(可选)
  "model": "string"          // AI模型(可选，默认: gpt-3.5-turbo)
}
```

**响应参数**:
```json
{
  "code": 200,
  "message": "创建成功",
  "data": {
    "sessionId": "session_123456",
    "title": "新会话",
    "model": "gpt-3.5-turbo",
    "createdAt": "2023-10-15T14:30:00Z"
  }
}
```

### 4.2 获取聊天会话列表
**GET** `/api/v1/chat/sessions`

**请求头**:
```
Authorization: Bearer {token}
```

**查询参数**:
```
?page=1&limit=20&sort=updated_at&order=desc
```

**响应参数**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "total": 50,
    "page": 1,
    "limit": 20,
    "list": [
      {
        "sessionId": "session_123456",
        "title": "合同审查讨论",
        "model": "gpt-3.5-turbo",
        "lastMessage": "请帮我分析这份合同",
        "lastMessageAt": "2023-10-15T14:30:00Z",
        "messageCount": 25,
        "createdAt": "2023-10-14T10:00:00Z"
      }
    ]
  }
}
```

### 4.3 发送消息
**POST** `/api/v1/chat/sessions/{sessionId}/messages`

**请求头**:
```
Authorization: Bearer {token}
```

**请求参数**:
```json
{
  "content": "string",       // 消息内容(必填)
  "type": "text",            // 消息类型: text, image, file
  "attachments": [{          // 附件(可选)
    "type": "file",
    "fileId": "file_123456"
  }]
}
```

**响应参数**:
```json
{
  "code": 200,
  "message": "发送成功",
  "data": {
    "messageId": "msg_123456",
    "sessionId": "session_123456",
    "content": "请帮我分析这份合同",
    "type": "text",
    "role": "user",
    "createdAt": "2023-10-15T14:30:00Z",
    "aiResponse": {
      "messageId": "msg_123457",
      "content": "我来帮您分析这份合同。首先，我需要查看合同的具体内容...",
      "role": "assistant",
      "createdAt": "2023-10-15T14:30:02Z"
    }
  }
}
```

### 4.4 获取消息历史
**GET** `/api/v1/chat/sessions/{sessionId}/messages`

**请求头**:
```
Authorization: Bearer {token}
```

**查询参数**:
```
?page=1&limit=50&before=message_id
```

**响应参数**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "total": 100,
    "page": 1,
    "limit": 50,
    "list": [
      {
        "messageId": "msg_123456",
        "content": "请帮我分析这份合同",
        "type": "text",
        "role": "user",
        "createdAt": "2023-10-15T14:30:00Z"
      },
      {
        "messageId": "msg_123457",
        "content": "我来帮您分析这份合同。首先，我需要查看合同的具体内容...",
        "type": "text",
        "role": "assistant",
        "createdAt": "2023-10-15T14:30:02Z"
      }
    ]
  }
}
```

### 4.5 删除会话
**DELETE** `/api/v1/chat/sessions/{sessionId}`

**请求头**:
```
Authorization: Bearer {token}
```

**响应参数**:
```json
{
  "code": 200,
  "message": "删除成功"
}
```

---

## 5. 数据统计接口

### 5.1 获取仪表板统计数据
**GET** `/api/v1/dashboard/stats`

**请求头**:
```
Authorization: Bearer {token}
```

**响应参数**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "totalVisits": 12345,
    "activeUsers": 567,
    "conversionRate": 89.5,
    "toolUsageStats": {
      "total": 2345,
      "today": 123,
      "thisWeek": 567,
      "thisMonth": 2345
    },
    "topTools": [
      {
        "toolId": "tool_001",
        "name": "合同审查助手",
        "usageCount": 1234
      }
    ]
  }
}
```

### 5.2 获取使用趋势
**GET** `/api/v1/dashboard/trends`

**请求头**:
```
Authorization: Bearer {token}
```

**查询参数**:
```
?period=7d&metric=visits  // period: 7d, 30d, 90d; metric: visits, users, tools
```

**响应参数**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "period": "7d",
    "metric": "visits",
    "data": [
      {
        "date": "2023-10-08",
        "value": 1200
      },
      {
        "date": "2023-10-09",
        "value": 1350
      }
    ]
  }
}
```

### 5.3 获取用户活动记录
**GET** `/api/v1/dashboard/activities`

**请求头**:
```
Authorization: Bearer {token}
```

**查询参数**:
```
?limit=20&types=tool_usage,chat,file_upload
```

**响应参数**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": [
    {
      "activityId": "activity_123456",
      "type": "tool_usage",
      "title": "合同分析报告",
      "description": "使用合同审查助手完成分析",
      "status": "completed",
      "createdAt": "2023-10-15T14:30:00Z"
    }
  ]
}
```

---

## 6. 系统设置接口

### 6.1 获取用户设置
**GET** `/api/v1/settings`

**请求头**:
```
Authorization: Bearer {token}
```

**响应参数**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "theme": "light",           // light, dark, auto
    "language": "zh-CN",        // zh-CN, en-US
    "notifications": {
      "desktop": true,
      "email": false,
      "sms": false
    },
    "privacy": {
      "shareData": false,
      "allowTracking": true
    }
  }
}
```

### 6.2 更新用户设置
**PUT** `/api/v1/settings`

**请求头**:
```
Authorization: Bearer {token}
```

**请求参数**:
```json
{
  "theme": "dark",
  "language": "en-US",
  "notifications": {
    "desktop": true,
    "email": true,
    "sms": false
  }
}
```

**响应参数**:
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "theme": "dark",
    "language": "en-US",
    "notifications": {
      "desktop": true,
      "email": true,
      "sms": false
    }
  }
}
```

### 6.3 获取系统配置
**GET** `/api/v1/settings/system`

**响应参数**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "maxFileSize": 104857600,     // 100MB
    "supportedFileTypes": ["pdf", "doc", "docx", "xls", "xlsx", "png", "jpg", "jpeg"],
    "aiModels": [
      {
        "id": "gpt-3.5-turbo",
        "name": "GPT-3.5 Turbo",
        "maxTokens": 4096
      }
    ],
    "toolCategories": [
      "management",
      "industrial",
      "llm",
      "data_analysis"
    ]
  }
}
```

---

## 7. 搜索接口

### 7.1 全局搜索
**GET** `/api/v1/search`

**请求头**:
```
Authorization: Bearer {token}
```

**查询参数**:
```
?q=keyword&type=all&page=1&limit=20
```

**响应参数**:
```json
{
  "code": 200,
  "message": "搜索成功",
  "data": {
    "total": 25,
    "page": 1,
    "limit": 20,
    "results": [
      {
        "type": "tool",
        "id": "tool_001",
        "title": "合同审查助手",
        "description": "智能合同审查工具",
        "relevance": 0.95
      },
      {
        "type": "file",
        "id": "file_123456",
        "title": "项目合同.pdf",
        "description": "2023年项目合同文档",
        "relevance": 0.87
      }
    ]
  }
}
```

### 7.2 搜索建议
**GET** `/api/v1/search/suggestions`

**查询参数**:
```
?q=contract&limit=10
```

**响应参数**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": [
    "合同审查",
    "合同分析",
    "合同模板",
    "合同管理"
  ]
}
```

---

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 429 | 请求频率限制 |
| 500 | 服务器内部错误 |
| 503 | 服务不可用 |

## 分页参数说明

所有列表接口都支持以下分页参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | int | 1 | 页码 |
| limit | int | 20 | 每页数量 |
| sort | string | created_at | 排序字段 |
| order | string | desc | 排序方式: asc, desc |

## 状态码说明

### 通用状态
- `active`: 活跃/启用
- `inactive`: 非活跃/禁用
- `deleted`: 已删除

### 任务状态
- `pending`: 等待中
- `processing`: 处理中
- `completed`: 已完成
- `failed`: 失败
- `cancelled`: 已取消

---

**最后更新**: 2023-10-15
**版本**: v1.0.0