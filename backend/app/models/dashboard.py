from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..db.database import Base

class DashboardStats(Base):
    __tablename__ = "dashboard_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    stat_type = Column(String(50), nullable=False)  # visits, users, conversion, etc.
    stat_value = Column(BigInteger, default=0)
    stat_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<DashboardStats(type='{self.stat_type}', value={self.stat_value})>"

class UserActivity(Base):
    __tablename__ = "user_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_type = Column(String(50), nullable=False)  # login, tool_use, file_upload, etc.
    activity_data = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关联用户
    user = relationship("User", backref="activities")
    
    def __repr__(self):
        return f"<UserActivity(user_id={self.user_id}, type='{self.activity_type}')>"