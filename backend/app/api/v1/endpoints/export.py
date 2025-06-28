"""
导出API端点
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.export_service import export_service
import logging
import os

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/articles/excel")
async def export_articles_to_excel(
    nickname: Optional[str] = Query(None, description="公众号名称，不提供则导出所有文章"),
    db: Session = Depends(get_db)
):
    """导出文章到Excel"""
    try:
        filepath = export_service.export_articles_to_excel(db, nickname)
        if filepath:
            return {
                "message": "导出成功",
                "filepath": filepath,
                "filename": os.path.basename(filepath)
            }
        else:
            raise HTTPException(status_code=400, detail="没有数据可导出")
    except Exception as e:
        logger.error(f"导出文章失败: {e}")
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@router.post("/likes/excel")
async def export_likes_to_excel(db: Session = Depends(get_db)):
    """导出收藏到Excel"""
    try:
        filepath = export_service.export_likes_to_excel(db)
        if filepath:
            return {
                "message": "导出成功",
                "filepath": filepath,
                "filename": os.path.basename(filepath)
            }
        else:
            raise HTTPException(status_code=400, detail="没有收藏数据可导出")
    except Exception as e:
        logger.error(f"导出收藏失败: {e}")
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@router.post("/search-results/excel")
async def export_search_results_to_excel(
    search_results: List[dict],
    search_keyword: str = Query(..., description="搜索关键词")
):
    """导出搜索结果到Excel"""
    try:
        filepath = export_service.export_search_results_to_excel(search_results, search_keyword)
        if filepath:
            return {
                "message": "导出成功",
                "filepath": filepath,
                "filename": os.path.basename(filepath)
            }
        else:
            raise HTTPException(status_code=400, detail="没有搜索结果可导出")
    except Exception as e:
        logger.error(f"导出搜索结果失败: {e}")
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@router.get("/files")
async def get_export_files():
    """获取导出文件列表"""
    try:
        files = export_service.get_export_files()
        return {"files": files}
    except Exception as e:
        logger.error(f"获取导出文件列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取文件列表失败")


@router.get("/download/{filename}")
async def download_export_file(filename: str):
    """下载导出文件"""
    try:
        filepath = os.path.join(export_service.output_folder, filename)
        if os.path.exists(filepath):
            return FileResponse(
                filepath,
                filename=filename,
                media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            raise HTTPException(status_code=404, detail="文件不存在")
    except Exception as e:
        logger.error(f"下载文件失败: {e}")
        raise HTTPException(status_code=500, detail="下载文件失败")


@router.delete("/files/{filename}")
async def delete_export_file(filename: str):
    """删除导出文件"""
    try:
        success = export_service.delete_export_file(filename)
        if success:
            return {"message": "删除文件成功"}
        else:
            raise HTTPException(status_code=404, detail="文件不存在")
    except Exception as e:
        logger.error(f"删除文件失败: {e}")
        raise HTTPException(status_code=500, detail="删除文件失败") 