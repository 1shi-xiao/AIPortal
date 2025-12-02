from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import logging
import os

from .core.config import settings
from .core.database import init_db
from .api import (
    auth_router,
    files_router,
    ai_tools_router,
    chat_router,
    dashboard_router,
    settings_router,
    search_router
)

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI门户系统后端API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# 全局异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": None
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "服务器内部错误",
            "data": None
        }
    )

# 注册API路由
app.include_router(auth_router, prefix="/api/v1")
app.include_router(files_router, prefix="/api/v1")
app.include_router(ai_tools_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(settings_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("正在启动AI门户后端服务...")
    
    try:
        # 初始化数据库
        init_db()
        logger.info("数据库初始化完成")
        
        # 初始化默认数据
        await init_default_data()
        logger.info("默认数据初始化完成")
        
        logger.info(f"服务启动成功，运行在 http://{settings.HOST}:{settings.PORT}")
        
    except Exception as e:
        logger.error(f"服务启动失败: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("正在关闭AI门户后端服务...")

async def init_default_data():
    """初始化默认数据"""
    from sqlalchemy.orm import Session
    from .core.database import SessionLocal
    from .models.tool import Tool
    
    db: Session = SessionLocal()
    
    try:
        # 检查是否已存在工具数据
        existing_tools = db.query(Tool).count()
        if existing_tools == 0:
            # 添加默认AI工具
            default_tools = [
                Tool(
                    tool_id="contract-review",
                    name="合同审查助手",
                    description="智能分析合同条款，识别潜在风险",
                    category="文档处理",
                    icon="document-text",
                    endpoint="/api/v1/ai-tools/contract-review/use"
                ),
                Tool(
                    tool_id="data-analysis",
                    name="数据分析工具",
                    description="自动化数据处理和可视化分析",
                    category="数据分析",
                    icon="chart-bar",
                    endpoint="/api/v1/ai-tools/data-analysis/use"
                ),
                Tool(
                    tool_id="image-style-transfer",
                    name="图片风格转换器",
                    description="将图片转换为不同的艺术风格",
                    category="图像处理",
                    icon="image",
                    endpoint="/api/v1/ai-tools/image-style-transfer/use"
                ),
                Tool(
                    tool_id="speech-to-text",
                    name="语音转文字助手",
                    description="高精度语音识别和转录服务",
                    category="语音处理",
                    icon="microphone",
                    endpoint="/api/v1/ai-tools/speech-to-text/use"
                ),
                Tool(
                    tool_id="code-completion",
                    name="代码智能补全器",
                    description="AI驱动的代码自动补全和优化建议",
                    category="编程辅助",
                    icon="code",
                    endpoint="/api/v1/ai-tools/code-completion/use"
                ),
                Tool(
                    tool_id="sentiment-analysis",
                    name="情感分析检测器",
                    description="分析文本情感倾向和情绪状态",
                    category="文本分析",
                    icon="emoji-happy",
                    endpoint="/api/v1/ai-tools/sentiment-analysis/use"
                )
            ]
            
            for tool in default_tools:
                db.add(tool)
            
            db.commit()
            logger.info(f"添加了 {len(default_tools)} 个默认AI工具")
    
    except Exception as e:
        logger.error(f"初始化默认数据失败: {str(e)}")
        db.rollback()
    finally:
        db.close()

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用AI门户系统API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    from datetime import datetime
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )