# 导入所有API路由
from .auth import router as auth_router
from .files import router as files_router
from .ai_tools import router as ai_tools_router
from .chat import router as chat_router
from .dashboard import router as dashboard_router
from .settings import router as settings_router
from .search import router as search_router

__all__ = [
    "auth_router",
    "files_router", 
    "ai_tools_router",
    "chat_router",
    "dashboard_router",
    "settings_router",
    "search_router"
]