"""
微信公众号账户模型
"""

from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class WechatAccount(Base):
    """微信公众号账户模型"""
    
    __tablename__ = "wechat_accounts"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    biz: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    nickname: Mapped[str] = mapped_column(String(200))
    account: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    avatar: Mapped[str] = mapped_column(String(500), nullable=True)
    qrcode: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # 统计信息
    article_count: Mapped[int] = mapped_column(Integer, default=0)
    follower_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # 状态信息
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # 时间信息
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_crawled_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # 关联关系
    articles: Mapped[list["Article"]] = relationship("Article", back_populates="account")
    
    def __repr__(self) -> str:
        return f"<WechatAccount(id={self.id}, nickname='{self.nickname}')>" 