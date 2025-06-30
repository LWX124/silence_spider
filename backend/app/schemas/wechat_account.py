"""
公众号相关的Pydantic模型
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class WechatAccountBase(BaseModel):
    """公众号基础模型"""
    biz: str = Field(..., description="公众号biz")
    nickname: str = Field(..., description="公众号名称")
    account: Optional[str] = Field(None, description="公众号账号")
    description: Optional[str] = Field(None, description="公众号描述")
    avatar: Optional[str] = Field(None, description="头像URL")
    qrcode: Optional[str] = Field(None, description="二维码URL")
    article_count: int = Field(0, description="文章数量")
    follower_count: int = Field(0, description="粉丝数量")
    is_verified: bool = Field(False, description="是否认证")
    is_active: bool = Field(True, description="是否激活")


class WechatAccountCreate(WechatAccountBase):
    """创建公众号模型"""
    pass


class WechatAccountUpdate(BaseModel):
    """更新公众号模型"""
    biz: Optional[str] = Field(None, description="公众号biz")
    nickname: Optional[str] = Field(None, description="公众号名称")
    account: Optional[str] = Field(None, description="公众号账号")
    description: Optional[str] = Field(None, description="公众号描述")
    avatar: Optional[str] = Field(None, description="头像URL")
    qrcode: Optional[str] = Field(None, description="二维码URL")
    article_count: Optional[int] = Field(None, description="文章数量")
    follower_count: Optional[int] = Field(None, description="粉丝数量")
    is_verified: Optional[bool] = Field(None, description="是否认证")
    is_active: Optional[bool] = Field(None, description="是否激活")


class WechatAccountResponse(WechatAccountBase):
    """公众号响应模型"""
    id: int = Field(..., description="公众号ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    last_crawled_at: Optional[datetime] = Field(None, description="最后爬取时间")

    class Config:
        from_attributes = True


class WechatAccountList(BaseModel):
    """公众号列表响应模型"""
    accounts: List[WechatAccountResponse] = Field(..., description="公众号列表")
    total: int = Field(..., description="总数")
    skip: int = Field(..., description="跳过数量")
    limit: int = Field(..., description="限制数量")


class WechatAccountStats(BaseModel):
    """公众号统计模型"""
    total_accounts: int = Field(..., description="总公众号数")
    active_accounts: int = Field(..., description="活跃公众号数")
    verified_accounts: int = Field(..., description="认证公众号数")
    total_articles: int = Field(..., description="总文章数") 