"""
搜索API端点
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.search_service import search_service
from app.schemas.search import SearchRequest, SearchResponse, IndexInfo
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/index-info", response_model=List[IndexInfo])
async def get_index_info():
    """获取搜索索引信息"""
    try:
        index_info = search_service.get_index_info()
        return index_info
    except Exception as e:
        logger.error(f"获取索引信息失败: {e}")
        raise HTTPException(status_code=500, detail="获取索引信息失败")


@router.post("/articles", response_model=SearchResponse)
async def search_articles(
    request: SearchRequest,
    db: Session = Depends(get_db)
):
    """搜索文章"""
    try:
        # 处理搜索范围
        gzhs = request.gzhs if request.gzhs and request.gzhs != ['全部'] else None
        
        # 处理搜索字段
        fields = request.fields if request.fields and '全部' not in request.fields else None
        
        result = search_service.search_articles(
            search_data=request.search_data,
            gzhs=gzhs,
            fields=fields,
            _from=request._from,
            _size=request._size
        )
        
        return SearchResponse(**result)
        
    except Exception as e:
        logger.error(f"搜索失败: {e}")
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")


@router.post("/create-index/{nickname}")
async def create_index(nickname: str):
    """为公众号创建搜索索引"""
    try:
        success = search_service.create_index(nickname)
        if success:
            return {"message": f"为公众号 {nickname} 创建索引成功"}
        else:
            raise HTTPException(status_code=500, detail="创建索引失败")
    except Exception as e:
        logger.error(f"创建索引失败: {e}")
        raise HTTPException(status_code=500, detail=f"创建索引失败: {str(e)}")


@router.delete("/delete-index/{nickname}")
async def delete_index(nickname: str):
    """删除公众号的搜索索引"""
    try:
        success = search_service.delete_index(nickname)
        if success:
            return {"message": f"删除公众号 {nickname} 的索引成功"}
        else:
            return {"message": f"公众号 {nickname} 的索引不存在"}
    except Exception as e:
        logger.error(f"删除索引失败: {e}")
        raise HTTPException(status_code=500, detail=f"删除索引失败: {str(e)}")


@router.post("/bulk-index/{nickname}")
async def bulk_index_articles(
    nickname: str,
    articles: List[dict],
    db: Session = Depends(get_db)
):
    """批量索引文章"""
    try:
        success = search_service.bulk_index_articles(nickname, articles)
        if success:
            return {"message": f"批量索引 {len(articles)} 篇文章成功"}
        else:
            raise HTTPException(status_code=500, detail="批量索引失败")
    except Exception as e:
        logger.error(f"批量索引失败: {e}")
        raise HTTPException(status_code=500, detail=f"批量索引失败: {str(e)}") 