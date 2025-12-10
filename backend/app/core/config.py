from pydantic import BaseModel
from typing import Optional, List
import os
import json
from dotenv import load_dotenv

# 先手动加载.env文件
load_dotenv()

# 辅助函数：解析环境变量，支持JSON和逗号分隔格式
def parse_env_list(value: str, default: List[str]) -> List[str]:
    if not value:
        return default
    # 尝试解析JSON格式
    if value.startswith('[') and value.endswith(']'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
    # 解析逗号分隔格式
    return [item.strip() for item in value.split(',')]

# 辅助函数：获取环境变量，支持类型转换
def get_env(key: str, default: any, type_cast: type = str) -> any:
    value = os.getenv(key)
    if value is None:
        return default
    if type_cast == bool:
        return value.lower() in ('true', '1', 'yes')
    if type_cast == int:
        return int(value)
    if type_cast == List:
        return parse_env_list(value, default)
    return type_cast(value)

class Settings(BaseModel):
    # 应用配置
    APP_NAME: str = get_env("APP_NAME", "AI Portal Backend")
    APP_VERSION: str = get_env("APP_VERSION", "1.0.0")
    DEBUG: bool = get_env("DEBUG", False, bool)
    
    # 服务器配置
    HOST: str = get_env("HOST", "0.0.0.0")
    PORT: int = get_env("PORT", 8000, int)
    
    # 数据库配置
    DATABASE_URL: str = get_env("DATABASE_URL", "sqlite:///./ai_portal.db")
    
    # JWT配置
    SECRET_KEY: str = get_env("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = get_env("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = get_env("ACCESS_TOKEN_EXPIRE_MINUTES", 30, int)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = get_env("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7, int)  # 7天
    
    # 文件上传配置
    UPLOAD_DIR: str = get_env("UPLOAD_DIR", "uploads")
    MAX_FILE_SIZE: int = get_env("MAX_FILE_SIZE", 100 * 1024 * 1024, int)  # 100MB
    ALLOWED_FILE_TYPES: List[str] = parse_env_list(
        os.getenv("ALLOWED_FILE_TYPES"),
        ["pdf", "doc", "docx", "xls", "xlsx", 
         "png", "jpg", "jpeg", "gif", "bmp",
         "txt", "md", "json", "csv"]
    )
    
    # AI服务配置
    OPENAI_API_KEY: Optional[str] = get_env("OPENAI_API_KEY", None)
    OPENAI_API_BASE: str = get_env("OPENAI_API_BASE", "https://api.openai.com/v1")
    DEFAULT_AI_MODEL: str = get_env("DEFAULT_AI_MODEL", "gpt-3.5-turbo")
    
    # 缓存配置
    REDIS_URL: Optional[str] = get_env("REDIS_URL", None)
    CACHE_TTL: int = get_env("CACHE_TTL", 3600, int)  # 1小时
    
    # 限流配置
    RATE_LIMIT_PER_MINUTE: int = get_env("RATE_LIMIT_PER_MINUTE", 60, int)
    RATE_LIMIT_PER_HOUR: int = get_env("RATE_LIMIT_PER_HOUR", 1000, int)
    
    # CORS配置
    CORS_ORIGINS: List[str] = parse_env_list(
        os.getenv("CORS_ORIGINS"),
        ["http://localhost:3000",
         "http://localhost:5173",
         "http://127.0.0.1:3000",
         "http://127.0.0.1:5173"]
    )
    
    # 日志配置
    LOG_LEVEL: str = get_env("LOG_LEVEL", "INFO")
    LOG_FILE: str = get_env("LOG_FILE", "logs/app.log")

# 创建配置实例
settings = Settings()

# 确保必要的目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)