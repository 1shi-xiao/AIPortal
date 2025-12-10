from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from ..core.security import get_password_hash, verify_password, create_tokens, get_current_user
from ..db.database import get_db
from ..models.user import User
from ..schemas import UserCreate, UserResponse, UserUpdate, BaseResponse, LoginRequest, Token, RefreshTokenRequest

router = APIRouter(prefix="/auth", tags=["认证"])

@router.post("/register", response_model=BaseResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 创建新用户
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password),
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return BaseResponse(
        message="注册成功",
        data={"user_id": db_user.id}
    )

@router.post("/login", response_model=BaseResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """用户登录"""
    # 查找用户
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.password_hash):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    if not user.is_active:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户已被禁用"
        )
    
    # 创建token
    tokens = create_tokens(str(user.id))
    
    # 更新最后登录时间
    user.last_login = datetime.now(timezone.utc)  # type: ignore
    db.commit()
    
    return BaseResponse(
        message="登录成功",
        data=tokens
    )

@router.post("/refresh", response_model=BaseResponse)
async def refresh_token(refresh_data: RefreshTokenRequest):
    """刷新访问令牌"""
    from ..core.security import verify_token
    
    user_id = verify_token(refresh_data.refresh_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )
    
    # 创建新的访问令牌
    tokens = create_tokens(user_id)
    
    return BaseResponse(
        message="令牌刷新成功",
        data=tokens
    )

@router.get("/me", response_model=BaseResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """获取当前用户信息"""
    return BaseResponse(
        message="获取用户信息成功",
        data=current_user
    )

@router.put("/me", response_model=BaseResponse)
async def update_current_user_info(
    user_update: UserUpdate, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新当前用户信息"""
    user = db.query(User).filter(User.id == current_user["id"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 更新用户信息
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return BaseResponse(
        message="更新用户信息成功",
        data=UserResponse.model_validate(user)
    )

@router.post("/logout", response_model=BaseResponse)
async def logout(current_user: dict = Depends(get_current_user)):
    """用户登出"""
    # 这里可以添加token黑名单逻辑
    return BaseResponse(message="登出成功")

@router.post("/change-password", response_model=BaseResponse)
async def change_password(
    old_password: str,
    new_password: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改密码"""
    user = db.query(User).filter(User.id == current_user["id"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 验证旧密码
    if not verify_password(old_password, user.password_hash):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="旧密码错误"
        )
    
    # 更新密码
    user.password_hash = get_password_hash(new_password)  # type: ignore
    db.commit()
    
    return BaseResponse(message="密码修改成功")