from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ...core.database import get_db
from ...core.security import get_current_user
from ...models import Tool, File, ChatSession, User
from ...schemas import SearchRequest, SearchResult, BaseResponse

router = APIRouter(prefix="/search", tags=["搜索"])

@router.get("/", response_model=BaseResponse)
async def search(
    q: str = Query(..., min_length=1, max_length=200, description="搜索关键词"),
    search_type: str = Query("all", description="搜索类型: all, tools, files, chats, users"),
    limit: int = Query(20, ge=1, le=100, description="返回结果数量限制"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """全局搜索"""
    results = []
    
    if search_type in ["all", "tools"]:
        # 搜索工具
        tools = db.query(Tool).filter(
            Tool.is_active == True,
            Tool.is_public == True
        ).filter(
            (Tool.name.contains(q)) |
            (Tool.description.contains(q)) |
            (Tool.category.contains(q))
        ).limit(limit // 2 if search_type == "all" else limit).all()
        
        for tool in tools:
            results.append(SearchResult(
                type="tool",
                id=str(tool.id),
                title=tool.name,
                description=tool.description,
                content=tool.category,
                score=calculate_relevance_score(q, tool.name, tool.description),
                metadata={
                    "category": tool.category,
                    "usage_count": tool.usage_count,
                    "created_at": tool.created_at.isoformat()
                }
            ))
    
    if search_type in ["all", "files"]:
        # 搜索文件
        files = db.query(File).filter(
            File.user_id == current_user["id"]
        ).filter(
            (File.original_name.contains(q)) |
            (File.file_type.contains(q))
        ).limit(limit // 3 if search_type == "all" else limit).all()
        
        for file in files:
            results.append(SearchResult(
                type="file",
                id=str(file.id),
                title=file.original_name,
                description=f"文件类型: {file.file_type.upper()}, 大小: {format_file_size(file.file_size)}",
                content=file.file_type,
                score=calculate_relevance_score(q, file.original_name),
                metadata={
                    "file_type": file.file_type,
                    "file_size": file.file_size,
                    "download_count": file.download_count,
                    "created_at": file.created_at.isoformat()
                }
            ))
    
    if search_type in ["all", "chats"]:
        # 搜索聊天记录
        from ...models.chat import ChatSession, ChatMessage
        
        # 搜索会话标题
        sessions = db.query(ChatSession).filter(
            ChatSession.user_id == current_user["id"],
            ChatSession.is_active == True,
            ChatSession.title.contains(q)
        ).limit(limit // 4 if search_type == "all" else limit).all()
        
        for session in sessions:
            results.append(SearchResult(
                type="chat",
                id=session.session_id,
                title=session.title,
                description=f"AI模型: {session.model_type}",
                content=session.title,
                score=calculate_relevance_score(q, session.title) * 0.9,  # 稍微降低聊天结果的权重
                metadata={
                    "model_type": session.model_type,
                    "updated_at": session.updated_at.isoformat() if session.updated_at else session.created_at.isoformat()
                }
            ))
        
        # 搜索聊天内容
        messages = db.query(ChatMessage).join(
            ChatSession, ChatMessage.session_id == ChatSession.id
        ).filter(
            ChatSession.user_id == current_user["id"],
            ChatSession.is_active == True,
            ChatMessage.content.contains(q)
        ).limit(limit // 4 if search_type == "all" else limit).all()
        
        for message in messages:
            results.append(SearchResult(
                type="chat",
                id=message.session.session_id,
                title=f"聊天记录: {message.session.title}",
                description=truncate_text(message.content, 100),
                content=message.content,
                score=calculate_relevance_score(q, message.content) * 0.8,
                metadata={
                    "role": message.role,
                    "created_at": message.created_at.isoformat(),
                    "session_title": message.session.title
                }
            ))
    
    # 按相关性排序
    results.sort(key=lambda x: x.score, reverse=True)
    
    return BaseResponse(
        message=f"搜索完成，找到 {len(results)} 个结果",
        data={
            "query": q,
            "type": search_type,
            "total": len(results),
            "results": results[:limit]
        }
    )

def calculate_relevance_score(query: str, *text_fields: str) -> float:
    """计算相关性分数"""
    query_lower = query.lower()
    total_score = 0.0
    
    for text in text_fields:
        if not text:
            continue
        
        text_lower = text.lower()
        
        # 完全匹配
        if query_lower == text_lower:
            total_score += 1.0
        # 开头匹配
        elif text_lower.startswith(query_lower):
            total_score += 0.8
        # 包含匹配
        elif query_lower in text_lower:
            total_score += 0.6
        # 单词匹配
        else:
            query_words = query_lower.split()
            text_words = text_lower.split()
            matching_words = sum(1 for word in query_words if word in text_words)
            if matching_words > 0:
                total_score += (matching_words / len(query_words)) * 0.4
    
    return min(total_score, 1.0)

def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024 and i < len(size_names) - 1:
        size /= 1024
        i += 1
    
    return f"{size:.1f} {size_names[i]}"

def truncate_text(text: str, max_length: int) -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

@router.get("/suggestions", response_model=BaseResponse)
async def get_search_suggestions(
    q: str = Query(..., min_length=1, max_length=50, description="输入的关键词"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取搜索建议"""
    if len(q) < 2:
        return BaseResponse(message="输入至少2个字符获取建议", data=[])
    
    suggestions = []
    
    # 工具名称建议
    tools = db.query(Tool.name).filter(
        Tool.is_active == True,
        Tool.is_public == True,
        Tool.name.startswith(q)
    ).limit(5).all()
    
    for tool in tools:
        suggestions.append({
            "type": "tool",
            "text": tool.name,
            "category": "工具"
        })
    
    # 文件名称建议
    files = db.query(File.original_name).filter(
        File.user_id == current_user["id"],
        File.original_name.startswith(q)
    ).limit(5).all()
    
    for file in files:
        suggestions.append({
            "type": "file",
            "text": file.original_name,
            "category": "文件"
        })
    
    # 会话标题建议
    from ...models.chat import ChatSession
    
    sessions = db.query(ChatSession.title).filter(
        ChatSession.user_id == current_user["id"],
        ChatSession.is_active == True,
        ChatSession.title.startswith(q)
    ).limit(5).all()
    
    for session in sessions:
        suggestions.append({
            "type": "chat",
            "text": session.title,
            "category": "聊天记录"
        })
    
    return BaseResponse(
        message="获取搜索建议成功",
        data=suggestions[:10]  # 最多返回10个建议
    )