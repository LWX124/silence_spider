"""
任务模型
"""

from datetime import datetime
from enum import Enum
from sqlalchemy import String, Integer, DateTime, Text, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TaskStatus(str, Enum):
    """任务状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskType(str, Enum):
    """任务类型枚举"""
    CRAWL_ACCOUNT = "crawl_account"
    CRAWL_ARTICLES = "crawl_articles"
    CRAWL_READING_DATA = "crawl_reading_data"
    EXPORT_DATA = "export_data"


class Task(Base):
    """任务模型"""
    
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # 基本信息
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    task_type: Mapped[TaskType] = mapped_column(SQLEnum(TaskType))
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.PENDING)
    
    # 任务参数
    parameters: Mapped[str] = mapped_column(Text, nullable=True)  # JSON格式存储参数
    
    # 进度信息
    progress: Mapped[int] = mapped_column(Integer, default=0)  # 0-100
    total_items: Mapped[int] = mapped_column(Integer, default=0)
    processed_items: Mapped[int] = mapped_column(Integer, default=0)
    
    # 结果信息
    result: Mapped[str] = mapped_column(Text, nullable=True)  # JSON格式存储结果
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    
    # 时间信息
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # 外键关联
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    user: Mapped["User"] = relationship("User")
    
    def __repr__(self) -> str:
        return f"<Task(id={self.id}, name='{self.name}', status='{self.status}')>" 