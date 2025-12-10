from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db.database import get_db
from ..core.security import get_current_user
from ..models.tool import Tool, ToolUsage
from ..schemas import ToolResponse, ToolUsageResponse, BaseResponse

router = APIRouter(prefix="/ai-tools", tags=["AI工具管理"])

@router.get("/", response_model=BaseResponse)
async def get_tools(
    category: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取AI工具列表"""
    query = db.query(Tool).filter(Tool.is_active == True)
    
    if category:
        query = query.filter(Tool.category == category)
    
    tools = query.offset(skip).limit(limit).all()
    
    return BaseResponse(
        message="获取工具列表成功",
        data=[ToolResponse.model_validate(tool) for tool in tools]
    )

@router.get("/{tool_id}", response_model=BaseResponse)
async def get_tool_detail(
    tool_id: str,
    db: Session = Depends(get_db)
):
    """获取工具详情"""
    tool = db.query(Tool).filter(
        Tool.tool_id == tool_id,
        Tool.is_active == True
    ).first()
    
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工具不存在"
        )
    
    return BaseResponse(
        message="获取工具详情成功",
        data=ToolResponse.model_validate(tool)
    )

@router.post("/{tool_id}/use", response_model=BaseResponse)
async def use_tool(
    tool_id: str,
    input_data: dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """使用AI工具"""
    tool = db.query(Tool).filter(
        Tool.tool_id == tool_id,
        Tool.is_active == True
    ).first()
    
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工具不存在"
        )
    
    # 这里应该调用具体的AI工具服务
    # 暂时返回模拟结果
    result = {
        "tool_id": tool_id,
        "result": f"工具 {tool.name} 的处理结果",
        "status": "success"
    }
    
    # 记录使用日志
    usage_record = ToolUsage(
        tool_id=tool.id,
        user_id=current_user["id"],
        usage_data=input_data,
        result_data=result
    )
    db.add(usage_record)
    
    # 更新工具使用次数
    from sqlalchemy import update
    stmt = update(Tool).where(Tool.id == tool.id).values(usage_count=Tool.usage_count + 1)
    db.execute(stmt)
    
    db.commit()
    
    return BaseResponse(
        message="工具使用成功",
        data=result
    )

@router.get("/{tool_id}/related", response_model=BaseResponse)
async def get_related_tools(
    tool_id: str,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """获取相关工具"""
    current_tool = db.query(Tool).filter(Tool.tool_id == tool_id).first()
    if not current_tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工具不存在"
        )
    
    # 获取同分类的其他工具
    related_tools = db.query(Tool).filter(
        Tool.category == current_tool.category,
        Tool.id != current_tool.id,
        Tool.is_active == True,
        Tool.is_public == True
    ).limit(limit).all()
    
    return BaseResponse(
        message="获取相关工具成功",
        data=[ToolResponse.model_validate(tool) for tool in related_tools]
    )

@router.get("/user/usage", response_model=BaseResponse)
async def get_user_tool_usage(
    skip: int = 0,
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的工具使用记录"""
    usage_records = db.query(ToolUsage).filter(
        ToolUsage.user_id == current_user["id"]
    ).order_by(ToolUsage.created_at.desc()).offset(skip).limit(limit).all()
    
    return BaseResponse(
        message="获取使用记录成功",
        data=[ToolUsageResponse.model_validate(record) for record in usage_records]
    )

@router.get("/categories", response_model=BaseResponse)
async def get_tool_categories(db: Session = Depends(get_db)):
    """获取工具分类"""
    from sqlalchemy import distinct
    
    categories = db.query(distinct(Tool.category)).filter(
        Tool.is_active == True
    ).all()
    
    category_list = [cat[0] for cat in categories if cat[0]]
    
    return BaseResponse(
        message="获取分类成功",
        data=category_list
    )

@router.get("/hot/list", response_model=BaseResponse)
async def get_hot_tools(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取热门工具"""
    hot_tools = db.query(Tool).filter(
        Tool.is_active == True,
        Tool.is_public == True
    ).order_by(Tool.usage_count.desc()).limit(limit).all()
    
    return BaseResponse(
        message="获取热门工具成功",
        data=[ToolResponse.model_validate(tool) for tool in hot_tools]
    )