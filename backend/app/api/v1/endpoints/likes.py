"""
收藏API端点
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.like_service import like_service
from app.schemas.like import LikeInfo, LikeList, LikeCreate, LikeDelete
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/info", response_model=LikeInfo)
async def get_like_info(db: Session = Depends(get_db)):
    """获取收藏统计信息"""
    try:
        return like_service.get_like_info(db)
    except Exception as e:
        logger.error(f"获取收藏信息失败: {e}")
        raise HTTPException(status_code=500, detail="获取收藏信息失败")


@router.get("/list", response_model=LikeList)
async def get_like_list(
    start: int = Query(0, ge=0, description="起始位置"),
    end: int = Query(10, ge=1, description="结束位置"),
    db: Session = Depends(get_db)
):
    """获取收藏文章列表"""
    try:
        likes = like_service.get_like_list(db, start, end)
        total = like_service.get_like_info(db)['total']
        
        return LikeList(
            total=total,
            articles=likes
        )
    except Exception as e:
        logger.error(f"获取收藏列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取收藏列表失败")


@router.post("/add")
async def add_like(
    like_data: LikeCreate,
    db: Session = Depends(get_db)
):
    """添加文章到收藏"""
    try:
        success = like_service.add_like(db, like_data.dict())
        if success:
            return {"message": "添加收藏成功"}
        else:
            raise HTTPException(status_code=400, detail="添加收藏失败，可能文章已收藏或不存在")
    except Exception as e:
        logger.error(f"添加收藏失败: {e}")
        raise HTTPException(status_code=500, detail=f"添加收藏失败: {str(e)}")


@router.delete("/delete")
async def delete_like(
    like_data: LikeDelete,
    db: Session = Depends(get_db)
):
    """从收藏中删除文章"""
    try:
        success = like_service.delete_like(db, like_data.dict())
        if success:
            return {"message": "删除收藏成功"}
        else:
            raise HTTPException(status_code=400, detail="删除收藏失败，收藏记录不存在")
    except Exception as e:
        logger.error(f"删除收藏失败: {e}")
        raise HTTPException(status_code=500, detail=f"删除收藏失败: {str(e)}")


@router.get("/search")
async def search_likes(
    keyword: str = Query(..., description="搜索关键词"),
    start: int = Query(0, ge=0, description="起始位置"),
    end: int = Query(10, ge=1, description="结束位置"),
    db: Session = Depends(get_db)
):
    """搜索收藏文章"""
    try:
        likes = like_service.search_likes(db, keyword, start, end)
        return {"results": likes}
    except Exception as e:
        logger.error(f"搜索收藏失败: {e}")
        raise HTTPException(status_code=500, detail="搜索收藏失败")


@router.get("/{like_id}")
async def get_like_detail(
    like_id: int,
    db: Session = Depends(get_db)
):
    """获取收藏详情"""
    try:
        like_detail = like_service.get_like_by_id(db, like_id)
        if like_detail:
            return like_detail
        else:
            raise HTTPException(status_code=404, detail="收藏记录不存在")
    except Exception as e:
        logger.error(f"获取收藏详情失败: {e}")
        raise HTTPException(status_code=500, detail="获取收藏详情失败")


@router.get("/export/all")
async def export_all_likes(db: Session = Depends(get_db)):
    """导出所有收藏数据"""
    try:
        likes_data = like_service.bulk_export_likes(db)
        return {"data": likes_data, "total": len(likes_data)}
    except Exception as e:
        logger.error(f"导出收藏数据失败: {e}")
        raise HTTPException(status_code=500, detail="导出收藏数据失败") 