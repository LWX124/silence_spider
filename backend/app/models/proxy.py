"""
代理模型
"""

from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Proxy(Base):
    """代理模型"""
    
    __tablename__ = "proxies"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # 代理信息
    host: Mapped[str] = mapped_column(String(100))
    port: Mapped[int] = mapped_column(Integer)
    protocol: Mapped[str] = mapped_column(String(10), default="http")  # http, https, socks5
    
    # 认证信息
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    password: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # 状态信息
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 性能指标
    response_time: Mapped[float] = mapped_column(Float, nullable=True)  # 响应时间(秒)
    success_rate: Mapped[float] = mapped_column(Float, default=0.0)  # 成功率(0-1)
    total_requests: Mapped[int] = mapped_column(Integer, default=0)
    success_requests: Mapped[int] = mapped_column(Integer, default=0)
    
    # 地理位置
    country: Mapped[str] = mapped_column(String(50), nullable=True)
    region: Mapped[str] = mapped_column(String(50), nullable=True)
    city: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # 时间信息
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_verified_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    @property
    def url(self) -> str:
        """获取代理URL"""
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"
    
    def __repr__(self) -> str:
        return f"<Proxy(id={self.id}, host='{self.host}:{self.port}')>" 