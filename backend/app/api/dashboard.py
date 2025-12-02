from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Dict, Any

from ...core.database import get_db
from ...core.security import get_current_user
from ...models.dashboard import DashboardStats, UserActivity
from ...models.user import User
from ...models.tool import Tool, ToolUsage
from ...schemas import DashboardStatsResponse, BaseResponse

router = APIRouter(prefix="/dashboard", tags=["数据统计"])

@router.get("/stats", response_model=BaseResponse)
async def get_dashboard_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取仪表板统计数据"""
    
    # 总访问量（最近30天）
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    total_visits = db.query(UserActivity).filter(
        UserActivity.created_at >= thirty_days_ago,
        UserActivity.activity_type == "login"
    ).count()
    
    # 总用户数
    total_users = db.query(User).filter(User.is_active == True).count()
    
    # 活跃用户（最近7天）
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    active_users = db.query(UserActivity.user_id).filter(
        UserActivity.created_at >= seven_days_ago
    ).distinct().count()
    
    # 转化率（注册用户中活跃用户的比例）
    conversion_rate = (active_users / total_users * 100) if total_users > 0 else 0
    
    # 工具使用统计
    tool_usage_stats = {}
    tool_usages = db.query(Tool.name, func.count(ToolUsage.id)).join(
        ToolUsage, Tool.id == ToolUsage.tool_id
    ).filter(
        ToolUsage.created_at >= thirty_days_ago
    ).group_by(Tool.name).all()
    
    for tool_name, usage_count in tool_usages:
        tool_usage_stats[tool_name] = usage_count
    
    # 最近活动
    recent_activities = db.query(UserActivity).order_by(
        UserActivity.created_at.desc()
    ).limit(10).all()
    
    activity_list = []
    for activity in recent_activities:
        activity_list.append({
            "id": activity.id,
            "user_id": activity.user_id,
            "type": activity.activity_type,
            "data": activity.activity_data,
            "created_at": activity.created_at.isoformat()
        })
    
    stats_data = DashboardStatsResponse(
        total_visits=total_visits,
        total_users=total_users,
        active_users=active_users,
        conversion_rate=round(conversion_rate, 2),
        tool_usage_stats=tool_usage_stats,
        recent_activities=activity_list
    )
    
    return BaseResponse(
        message="获取统计数据成功",
        data=stats_data
    )

@router.get("/user/stats", response_model=BaseResponse)
async def get_user_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户个人统计数据"""
    user_id = current_user["id"]
    
    # 用户活动统计（最近30天）
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    user_activities = db.query(UserActivity).filter(
        UserActivity.user_id == user_id,
        UserActivity.created_at >= thirty_days_ago
    ).all()
    
    # 按活动类型分组
    activity_stats = {}
    for activity in user_activities:
        activity_type = activity.activity_type
        if activity_type not in activity_stats:
            activity_stats[activity_type] = 0
        activity_stats[activity_type] += 1
    
    # 工具使用统计
    tool_usages = db.query(Tool.name, func.count(ToolUsage.id)).join(
        ToolUsage, Tool.id == ToolUsage.tool_id
    ).filter(
        ToolUsage.user_id == user_id,
        ToolUsage.created_at >= thirty_days_ago
    ).group_by(Tool.name).all()
    
    tool_stats = {tool_name: count for tool_name, count in tool_usages}
    
    user_stats = {
        "total_activities": len(user_activities),
        "activity_breakdown": activity_stats,
        "tool_usage": tool_stats,
        "most_active_day": get_most_active_day(user_activities),
        "join_days": (datetime.utcnow() - current_user.get("created_at", datetime.utcnow())).days
    }
    
    return BaseResponse(
        message="获取用户统计成功",
        data=user_stats
    )

def get_most_active_day(activities):
    """获取最活跃的一天"""
    if not activities:
        return None
    
    day_counts = {}
    for activity in activities:
        day = activity.created_at.date()
        day_counts[day] = day_counts.get(day, 0) + 1
    
    most_active_day = max(day_counts.items(), key=lambda x: x[1])[0]
    return most_active_day.isoformat()

@router.post("/activity", response_model=BaseResponse)
async def record_activity(
    activity_type: str,
    activity_data: Dict[str, Any] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """记录用户活动"""
    activity = UserActivity(
        user_id=current_user["id"],
        activity_type=activity_type,
        activity_data=str(activity_data) if activity_data else None
    )
    
    db.add(activity)
    db.commit()
    
    return BaseResponse(message="活动记录成功")

@router.get("/trends", response_model=BaseResponse)
async def get_trends(
    days: int = 30,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取趋势数据"""
    if days < 1 or days > 365:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="天数必须在1-365之间"
        )
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # 按天统计访问量
    daily_visits = db.query(
        func.date(UserActivity.created_at).label('date'),
        func.count(UserActivity.id).label('count')
    ).filter(
        UserActivity.created_at >= start_date,
        UserActivity.created_at <= end_date,
        UserActivity.activity_type == "login"
    ).group_by(
        func.date(UserActivity.created_at)
    ).order_by(
        func.date(UserActivity.created_at)
    ).all()
    
    # 按天统计工具使用
    daily_tool_usage = db.query(
        func.date(ToolUsage.created_at).label('date'),
        func.count(ToolUsage.id).label('count')
    ).filter(
        ToolUsage.created_at >= start_date,
        ToolUsage.created_at <= end_date
    ).group_by(
        func.date(ToolUsage.created_at)
    ).order_by(
        func.date(ToolUsage.created_at)
    ).all()
    
    trends_data = {
        "daily_visits": [{"date": str(item.date), "count": item.count} for item in daily_visits],
        "daily_tool_usage": [{"date": str(item.date), "count": item.count} for item in daily_tool_usage],
        "period": f"{start_date.date()} to {end_date.date()}"
    }
    
    return BaseResponse(
        message="获取趋势数据成功",
        data=trends_data
    )