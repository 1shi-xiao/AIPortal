from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from ...core.database import get_db
from ...core.security import get_current_user
from ...models.chat import ChatSession, ChatMessage
from ...schemas import (
    ChatSessionCreate, 
    ChatSessionResponse, 
    ChatMessageResponse, 
    ChatMessageCreate,
    BaseResponse
)

router = APIRouter(prefix="/chat", tags=["AI聊天"])

@router.post("/sessions", response_model=BaseResponse)
async def create_chat_session(
    session_data: ChatSessionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建聊天会话"""
    # 生成唯一的会话ID
    session_id = str(uuid.uuid4())
    
    db_session = ChatSession(
        session_id=session_id,
        user_id=current_user["id"],
        title=session_data.title or "新会话",
        model_type=session_data.model_type
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return BaseResponse(
        message="创建会话成功",
        data=ChatSessionResponse.from_orm(db_session)
    )

@router.get("/sessions", response_model=BaseResponse)
async def get_chat_sessions(
    skip: int = 0,
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的聊天会话列表"""
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user["id"],
        ChatSession.is_active == True
    ).order_by(ChatSession.updated_at.desc()).offset(skip).limit(limit).all()
    
    return BaseResponse(
        message="获取会话列表成功",
        data=[ChatSessionResponse.from_orm(session) for session in sessions]
    )

@router.get("/sessions/{session_id}", response_model=BaseResponse)
async def get_chat_session(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取聊天会话详情"""
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id,
        ChatSession.user_id == current_user["id"]
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )
    
    return BaseResponse(
        message="获取会话详情成功",
        data=ChatSessionResponse.from_orm(session)
    )

@router.delete("/sessions/{session_id}", response_model=BaseResponse)
async def delete_chat_session(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除聊天会话"""
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id,
        ChatSession.user_id == current_user["id"]
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )
    
    # 软删除，标记为不活跃
    session.is_active = False
    db.commit()
    
    return BaseResponse(message="删除会话成功")

@router.get("/sessions/{session_id}/messages", response_model=BaseResponse)
async def get_chat_messages(
    session_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取聊天消息"""
    # 验证会话所有权
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id,
        ChatSession.user_id == current_user["id"]
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )
    
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session.id
    ).order_by(ChatMessage.created_at.asc()).offset(skip).limit(limit).all()
    
    return BaseResponse(
        message="获取消息成功",
        data=[ChatMessageResponse.from_orm(msg) for msg in messages]
    )

@router.post("/sessions/{session_id}/messages", response_model=BaseResponse)
async def send_message(
    session_id: str,
    message_data: ChatMessageCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """发送聊天消息"""
    # 验证会话所有权
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id,
        ChatSession.user_id == current_user["id"]
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )
    
    # 保存用户消息
    user_message = ChatMessage(
        session_id=session.id,
        role="user",
        content=message_data.content
    )
    db.add(user_message)
    
    # 这里应该调用AI服务生成回复
    # 暂时返回模拟的AI回复
    ai_reply = f"这是AI助手对您的消息 '{message_data.content}' 的回复。"
    
    # 保存AI回复
    ai_message = ChatMessage(
        session_id=session.id,
        role="assistant",
        content=ai_reply
    )
    db.add(ai_message)
    
    # 更新会话时间
    session.updated_at = datetime.utcnow()
    
    db.commit()
    
    return BaseResponse(
        message="消息发送成功",
        data={
            "user_message": ChatMessageResponse.from_orm(user_message),
            "ai_message": ChatMessageResponse.from_orm(ai_message)
        }
    )

@router.post("/sessions/{session_id}/clear", response_model=BaseResponse)
async def clear_chat_session(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """清空聊天记录"""
    # 验证会话所有权
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id,
        ChatSession.user_id == current_user["id"]
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )
    
    # 删除所有消息
    db.query(ChatMessage).filter(ChatMessage.session_id == session.id).delete()
    db.commit()
    
    return BaseResponse(message="清空聊天记录成功")

@router.get("/models", response_model=BaseResponse)
async def get_available_models():
    """获取可用的AI模型"""
    models = [
        {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "快速高效的通用模型"},
        {"id": "gpt-4", "name": "GPT-4", "description": "更强大的推理能力"},
        {"id": "claude-3-sonnet", "name": "Claude 3 Sonnet", "description": "平衡性能和成本"},
        {"id": "claude-3-opus", "name": "Claude 3 Opus", "description": "顶级推理能力"}
    ]
    
    return BaseResponse(
        message="获取模型列表成功",
        data=models
    )