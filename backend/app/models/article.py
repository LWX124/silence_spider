"""
文章模型
"""

from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Text, Boolean, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Article(Base):
    """文章模型"""
    
    __tablename__ = "articles"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # 基本信息
    title: Mapped[str] = mapped_column(String(500))
    author: Mapped[str] = mapped_column(String(100), nullable=True)
    digest: Mapped[str] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    content_html: Mapped[str] = mapped_column(Text, nullable=True)
    
    # 链接信息
    url: Mapped[str] = mapped_column(String(1000), unique=True, index=True)
    cover_url: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    # 微信特有字段
    biz: Mapped[str] = mapped_column(String(100), index=True)
    mid: Mapped[str] = mapped_column(String(100), index=True)
    idx: Mapped[int] = mapped_column(Integer, default=0)
    sn: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # 时间信息
    publish_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 统计数据
    read_num: Mapped[int] = mapped_column(Integer, default=0)
    like_num: Mapped[int] = mapped_column(Integer, default=0)
    reward_num: Mapped[int] = mapped_column(Integer, default=0)
    comment_num: Mapped[int] = mapped_column(Integer, default=0)
    
    # 位置信息
    position: Mapped[int] = mapped_column(Integer, default=0)  # 头条、次条等
    ip_location: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # 状态信息
    is_original: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 外键关联
    account_id: Mapped[int] = mapped_column(ForeignKey("wechat_accounts.id"), index=True)
    account: Mapped["WechatAccount"] = relationship("WechatAccount", back_populates="articles")
    
    def __repr__(self) -> str:
        return f"<Article(id={self.id}, title='{self.title[:50]}...')>" 