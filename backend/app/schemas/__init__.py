from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# 基础响应模型
class BaseResponse(BaseModel):
    success: bool = True
    message: str = "操作成功"
    data: Optional[Any] = None

# 用户相关模型
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    full_name: Optional[str] = Field(None, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = None
    full_name: Optional[str] = Field(None, max_length=100)
    avatar: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 认证相关模型
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# 文件相关模型
class FileBase(BaseModel):
    filename: str
    original_name: str
    file_size: int
    file_type: str
    mime_type: Optional[str] = None

class FileCreate(FileBase):
    user_id: int
    file_path: str

class FileResponse(FileBase):
    id: int
    user_id: int
    file_path: str
    download_count: int
    is_public: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# 聊天相关模型
class ChatMessageBase(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str

class ChatMessageCreate(ChatMessageBase):
    session_id: int

class ChatMessageResponse(ChatMessageBase):
    id: int
    session_id: int
    tokens: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatSessionBase(BaseModel):
    title: Optional[str] = None
    model_type: str = "gpt-3.5-turbo"

class ChatSessionCreate(ChatSessionBase):
    user_id: int

class ChatSessionResponse(ChatSessionBase):
    id: int
    session_id: str
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 工具相关模型
class ToolBase(BaseModel):
    tool_id: str
    name: str
    description: Optional[str] = None
    category: str
    icon: Optional[str] = None
    endpoint: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

class ToolCreate(ToolBase):
    pass

class ToolResponse(ToolBase):
    id: int
    is_active: bool
    is_public: bool
    usage_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ToolUsageBase(BaseModel):
    tool_id: int
    user_id: int
    usage_data: Optional[Dict[str, Any]] = None
    result_data: Optional[Dict[str, Any]] = None

class ToolUsageCreate(ToolUsageBase):
    pass

class ToolUsageResponse(ToolUsageBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 仪表板相关模型
class DashboardStatsResponse(BaseModel):
    total_visits: int
    total_users: int
    active_users: int
    conversion_rate: float
    tool_usage_stats: Dict[str, int]
    recent_activities: List[Dict[str, Any]]

# 设置相关模型
class UserSettingsBase(BaseModel):
    theme: str = "light"
    language: str = "zh-CN"
    notifications: Dict[str, bool] = {
        "email": True,
        "push": False,
        "sms": False
    }
    privacy: Dict[str, bool] = {
        "profile_visible": True,
        "activity_visible": False
    }
    ai_preferences: Dict[str, Any] = {
        "default_model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 1000
    }

class UserSettingsCreate(UserSettingsBase):
    user_id: int

class UserSettingsResponse(UserSettingsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class SystemSettingsBase(BaseModel):
    setting_key: str
    setting_value: Optional[str] = None
    setting_type: str = "string"
    description: Optional[str] = None
    is_public: bool = False

class SystemSettingsCreate(SystemSettingsBase):
    pass

class SystemSettingsResponse(SystemSettingsBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 搜索相关模型
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=200)
    search_type: str = "all"  # all, tools, files, chats
    limit: int = Field(20, ge=1, le=100)

class SearchResult(BaseModel):
    type: str  # tool, file, chat, user
    id: str
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    score: float
    metadata: Optional[Dict[str, Any]] = None