"""
收藏模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Like(Base):
    """收藏表"""
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(255), nullable=False, comment="公众号名称")
    title = Column(String(500), nullable=False, comment="文章标题")
    author = Column(String(255), comment="作者")
    content_url = Column(String(1000), nullable=False, unique=True, comment="文章链接")
    source_url = Column(String(1000), comment="原文链接")
    p_date = Column(DateTime, comment="发布时间")
    like_time = Column(DateTime, default=func.now(), comment="收藏时间")
    read_num = Column(Integer, default=0, comment="阅读数")
    like_num = Column(Integer, default=0, comment="点赞数")
    comment_num = Column(Integer, default=0, comment="评论数")
    reward_num = Column(Integer, default=0, comment="赞赏数")
    digest = Column(Text, comment="摘要")
    content = Column(Text, comment="文章内容")
    
    def __repr__(self):
        return f"<Like(id={self.id}, title='{self.title}', nickname='{self.nickname}')>" 