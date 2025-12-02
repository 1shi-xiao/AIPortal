from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..db.database import Base

class Tool(Base):
    __tablename__ = "tools"
    
    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)
    icon = Column(String(255), nullable=True)
    endpoint = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=True)
    config = Column(JSON, nullable=True)  # 工具配置
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联用户使用记录
    usage_records = relationship("ToolUsage", backref="tool")
    
    def __repr__(self):
        return f"<Tool(tool_id='{self.tool_id}', name='{self.name}')>"

class ToolUsage(Base):
    __tablename__ = "tool_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, ForeignKey("tools.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    usage_data = Column(JSON, nullable=True)  # 使用数据
    result_data = Column(JSON, nullable=True)  # 结果数据
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关联用户
    user = relationship("User", backref="tool_usage")
    
    def __repr__(self):
        return f"<ToolUsage(tool_id={self.tool_id}, user_id={self.user_id})>"