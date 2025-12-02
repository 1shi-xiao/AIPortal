from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..db.database import Base

class UserSettings(Base):
    __tablename__ = "user_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    theme = Column(String(20), default="light")  # light, dark, auto
    language = Column(String(10), default="zh-CN")  # zh-CN, en-US
    notifications = Column(JSON, default={
        "email": True,
        "push": False,
        "sms": False
    })
    privacy = Column(JSON, default={
        "profile_visible": True,
        "activity_visible": False
    })
    ai_preferences = Column(JSON, default={
        "default_model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 1000
    })
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联用户
    user = relationship("User", backref="settings", uselist=False)
    
    def __repr__(self):
        return f"<UserSettings(user_id={self.user_id}, theme='{self.theme}')>"

class SystemSettings(Base):
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String(100), unique=True, index=True, nullable=False)
    setting_value = Column(Text, nullable=True)
    setting_type = Column(String(20), default="string")  # string, json, boolean, number
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=False)  # 是否对用户可见
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<SystemSettings(key='{self.setting_key}', type='{self.setting_type}')>"