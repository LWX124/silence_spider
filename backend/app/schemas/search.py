"""
搜索相关的Pydantic模型
"""

from typing import List, Optional, Any
from pydantic import BaseModel


class SearchRequest(BaseModel):
    """搜索请求模型"""
    query: str
    page: int = 1
    size: int = 10
    filters: Optional[dict] = None


class SearchResponse(BaseModel):
    """搜索响应模型"""
    results: List[Any]
    total: int
    page: int
    size: int
    query: str


class IndexInfo(BaseModel):
    """索引信息模型"""
    name: str
    document_count: int
    size: str
    status: str 