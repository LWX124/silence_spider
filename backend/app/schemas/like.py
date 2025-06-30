"""
点赞相关的Pydantic模型
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class LikeInfo(BaseModel):
    """点赞信息模型"""
    id: int
    user_id: int
    article_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class LikeCreate(BaseModel):
    """创建点赞模型"""
    article_id: str


class LikeDelete(BaseModel):
    """删除点赞模型"""
    article_id: str


class LikeList(BaseModel):
    """点赞列表模型"""
    likes: List[LikeInfo]
    total: int
    page: int
    size: int 