from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from datetime import datetime

from ...core.database import get_db
from ...core.security import get_current_user
from ...models.file import File as FileModel
from ...schemas import FileCreate, FileResponse, BaseResponse
from ...core.config import settings

router = APIRouter(prefix="/files", tags=["文件管理"])

@router.post("/upload", response_model=BaseResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上传文件"""
    # 检查文件大小
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"文件大小超过限制 ({settings.MAX_FILE_SIZE // (1024*1024)}MB)"
        )
    
    # 检查文件类型
    file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    if file_extension not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型。支持的类型: {', '.join(settings.ALLOWED_FILE_TYPES)}"
        )
    
    # 生成唯一文件名
    unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    # 创建文件记录
    db_file = FileModel(
        filename=unique_filename,
        original_name=file.filename,
        file_path=file_path,
        file_size=file_size,
        file_type=file_extension,
        mime_type=file.content_type,
        user_id=current_user["id"]
    )
    
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    return BaseResponse(
        message="文件上传成功",
        data=FileResponse.from_orm(db_file)
    )

@router.get("/", response_model=BaseResponse)
async def get_user_files(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户文件列表"""
    files = db.query(FileModel).filter(
        FileModel.user_id == current_user["id"]
    ).offset(skip).limit(limit).all()
    
    return BaseResponse(
        message="获取文件列表成功",
        data=[FileResponse.from_orm(file) for file in files]
    )

@router.get("/{file_id}", response_model=BaseResponse)
async def get_file_info(
    file_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取文件信息"""
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.user_id == current_user["id"]
    ).first()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    
    return BaseResponse(
        message="获取文件信息成功",
        data=FileResponse.from_orm(file)
    )

@router.delete("/{file_id}", response_model=BaseResponse)
async def delete_file(
    file_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除文件"""
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.user_id == current_user["id"]
    ).first()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    
    # 删除物理文件
    if os.path.exists(file.file_path):
        os.remove(file.file_path)
    
    # 删除数据库记录
    db.delete(file)
    db.commit()
    
    return BaseResponse(message="文件删除成功")

@router.get("/{file_id}/download")
async def download_file(
    file_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """下载文件"""
    from fastapi.responses import FileResponse
    
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.user_id == current_user["id"]
    ).first()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    
    # 检查文件是否存在
    if not os.path.exists(file.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在或已被删除"
        )
    
    # 更新下载次数
    file.download_count += 1
    db.commit()
    
    return FileResponse(
        path=file.file_path,
        filename=file.original_name,
        media_type=file.mime_type or "application/octet-stream"
    )

@router.post("/{file_id}/share", response_model=BaseResponse)
async def share_file(
    file_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """分享文件"""
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.user_id == current_user["id"]
    ).first()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    
    # 设置为公开分享
    file.is_public = True
    db.commit()
    
    share_url = f"{settings.HOST}/api/v1/files/{file_id}/public"
    
    return BaseResponse(
        message="文件分享成功",
        data={"share_url": share_url}
    )

@router.get("/{file_id}/public")
async def get_public_file(file_id: int, db: Session = Depends(get_db)):
    """获取公开文件"""
    from fastapi.responses import FileResponse
    
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.is_public == True
    ).first()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在或未公开分享"
        )
    
    # 检查文件是否存在
    if not os.path.exists(file.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在或已被删除"
        )
    
    return FileResponse(
        path=file.file_path,
        filename=file.original_name,
        media_type=file.mime_type or "application/octet-stream"
    )