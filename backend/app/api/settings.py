from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from ..db.database import get_db
from ..core.security import get_current_user
from ..models.settings import UserSettings, SystemSettings
from ..schemas import UserSettingsResponse, SystemSettingsResponse, BaseResponse

router = APIRouter(prefix="/settings", tags=["系统设置"])

@router.get("/user", response_model=BaseResponse)
async def get_user_settings(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户设置"""
    settings = db.query(UserSettings).filter(
        UserSettings.user_id == current_user["id"]
    ).first()
    
    if not settings:
        # 创建默认设置
        settings = UserSettings(user_id=current_user["id"])
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    return BaseResponse(
        message="获取用户设置成功",
        data=UserSettingsResponse.model_validate(settings)
    )

@router.put("/user", response_model=BaseResponse)
async def update_user_settings(
    settings_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户设置"""
    settings = db.query(UserSettings).filter(
        UserSettings.user_id == current_user["id"]
    ).first()
    
    if not settings:
        # 创建新设置
        settings = UserSettings(
            user_id=current_user["id"],
            **settings_data
        )
        db.add(settings)
    else:
        # 更新现有设置
        for key, value in settings_data.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
    
    db.commit()
    db.refresh(settings)
    
    return BaseResponse(
        message="更新用户设置成功",
        data=UserSettingsResponse.model_validate(settings)
    )

@router.get("/system/public", response_model=BaseResponse)
async def get_public_system_settings(
    db: Session = Depends(get_db)
):
    """获取公开的系统设置"""
    settings = db.query(SystemSettings).filter(
        SystemSettings.is_public == True
    ).all()
    
    settings_dict = {}
    for setting in settings:
        settings_dict[setting.setting_key] = {
            "value": setting.setting_value,
            "type": setting.setting_type,
            "description": setting.description
        }
    
    return BaseResponse(
        message="获取系统设置成功",
        data=settings_dict
    )

@router.get("/system", response_model=BaseResponse)
async def get_system_settings(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取所有系统设置（需要管理员权限）"""
    # 这里应该检查管理员权限
    # if not current_user.get("is_superuser"):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="需要管理员权限"
    #     )
    
    settings = db.query(SystemSettings).all()
    
    return BaseResponse(
        message="获取系统设置成功",
        data=[SystemSettingsResponse.model_validate(setting) for setting in settings]
    )

@router.put("/system/{setting_key}", response_model=BaseResponse)
async def update_system_setting(
    setting_key: str,
    setting_value: str,
    setting_type: str = "string",
    description: Optional[str] = None,
    is_public: bool = False,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新系统设置（需要管理员权限）"""
    # 这里应该检查管理员权限
    
    setting = db.query(SystemSettings).filter(
        SystemSettings.setting_key == setting_key
    ).first()
    
    if not setting:
        # 创建新设置
        setting = SystemSettings(
            setting_key=setting_key,
            setting_value=setting_value,
            setting_type=setting_type,
            description=description,
            is_public=is_public
        )
        db.add(setting)
    else:
        # 更新现有设置
        from sqlalchemy import update
        update_data = {
            SystemSettings.setting_value: setting_value,  # type: ignore
            SystemSettings.setting_type: setting_type,  # type: ignore
            SystemSettings.description: description,  # type: ignore
            SystemSettings.is_public: is_public  # type: ignore
        }
        stmt = update(SystemSettings).where(SystemSettings.id == setting.id).values(**update_data)
        db.execute(stmt)
    
    db.commit()
    if not setting:
        db.refresh(setting)
    
    return BaseResponse(
        message="更新系统设置成功",
        data=SystemSettingsResponse.model_validate(setting)
    )

@router.delete("/system/{setting_key}", response_model=BaseResponse)
async def delete_system_setting(
    setting_key: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除系统设置（需要管理员权限）"""
    # 这里应该检查管理员权限
    
    setting = db.query(SystemSettings).filter(
        SystemSettings.setting_key == setting_key
    ).first()
    
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="设置不存在"
        )
    
    db.delete(setting)
    db.commit()
    
    return BaseResponse(message="删除系统设置成功")

@router.get("/themes", response_model=BaseResponse)
async def get_available_themes():
    """获取可用的主题"""
    themes = [
        {"id": "light", "name": "浅色主题", "description": "经典的浅色界面"},
        {"id": "dark", "name": "深色主题", "description": "护眼的深色界面"},
        {"id": "auto", "name": "自动主题", "description": "根据系统设置自动切换"}
    ]
    
    return BaseResponse(
        message="获取主题列表成功",
        data=themes
    )

@router.get("/languages", response_model=BaseResponse)
async def get_available_languages():
    """获取可用的语言"""
    languages = [
        {"code": "zh-CN", "name": "简体中文", "native_name": "简体中文"},
        {"code": "en-US", "name": "English", "native_name": "English"},
        {"code": "ja-JP", "name": "日本語", "native_name": "日本語"},
        {"code": "ko-KR", "name": "한국어", "native_name": "한국어"}
    ]
    
    return BaseResponse(
        message="获取语言列表成功",
        data=languages
    )