"""
收藏服务
管理文章收藏功能
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.article import Article
from app.models.like import Like
from app.core.database import get_db

logger = logging.getLogger(__name__)


class LikeService:
    """收藏服务类"""
    
    def __init__(self):
        pass
    
    def get_like_info(self, db: Session) -> Dict[str, Any]:
        """获取收藏统计信息"""
        try:
            total_count = db.query(Like).count()
            return {
                'total': total_count,
                'updated_at': datetime.now()
            }
        except Exception as e:
            logger.error(f"获取收藏信息失败: {e}")
            return {'total': 0, 'error': str(e)}
    
    def get_like_list(self, db: Session, start: int = 0, end: int = 10) -> List[Dict[str, Any]]:
        """获取收藏文章列表"""
        try:
            likes = db.query(Like).order_by(Like.like_time.desc()).offset(start).limit(end - start).all()
            
            result = []
            for like in likes:
                like_data = {
                    'id': like.id,
                    'nickname': like.nickname,
                    'title': like.title,
                    'author': like.author,
                    'content_url': like.content_url,
                    'source_url': like.source_url,
                    'p_date': like.p_date,
                    'like_time': like.like_time,
                    'read_num': like.read_num,
                    'like_num': like.like_num,
                    'comment_num': like.comment_num,
                    'reward_num': like.reward_num,
                    'digest': like.digest,
                    'content': like.content
                }
                result.append(like_data)
            
            return result
        except Exception as e:
            logger.error(f"获取收藏列表失败: {e}")
            return []
    
    def add_like(self, db: Session, article_info: Dict[str, Any]) -> bool:
        """添加文章到收藏"""
        try:
            nickname = article_info.get('nickname')
            content_url = article_info.get('content_url')
            
            # 检查是否已经收藏
            existing_like = db.query(Like).filter(
                Like.nickname == nickname,
                Like.content_url == content_url
            ).first()
            
            if existing_like:
                logger.warning(f"文章已收藏: {content_url}")
                return False
            
            # 从文章表获取完整信息
            article = db.query(Article).filter(
                Article.nickname == nickname,
                Article.content_url == content_url
            ).first()
            
            if not article:
                logger.error(f"文章不存在: {content_url}")
                return False
            
            # 创建收藏记录
            like = Like(
                nickname=article.nickname,
                title=article.title,
                author=article.author,
                content_url=article.content_url,
                source_url=article.source_url,
                p_date=article.p_date,
                like_time=datetime.now(),
                read_num=article.read_num,
                like_num=article.like_num,
                comment_num=article.comment_num,
                reward_num=article.reward_num,
                digest=article.digest,
                content=article.content
            )
            
            db.add(like)
            
            # 更新原文章的收藏状态
            article.like_folder = True
            db.commit()
            
            logger.info(f"添加收藏成功: {content_url}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"添加收藏失败: {e}")
            return False
    
    def delete_like(self, db: Session, article_info: Dict[str, Any]) -> bool:
        """从收藏中删除文章"""
        try:
            nickname = article_info.get('nickname')
            content_url = article_info.get('content_url')
            
            # 删除收藏记录
            like = db.query(Like).filter(
                Like.nickname == nickname,
                Like.content_url == content_url
            ).first()
            
            if not like:
                logger.warning(f"收藏记录不存在: {content_url}")
                return False
            
            db.delete(like)
            
            # 更新原文章的收藏状态
            article = db.query(Article).filter(
                Article.nickname == nickname,
                Article.content_url == content_url
            ).first()
            
            if article:
                article.like_folder = False
            
            db.commit()
            
            logger.info(f"删除收藏成功: {content_url}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"删除收藏失败: {e}")
            return False
    
    def search_likes(self, db: Session, search_data: str, start: int = 0, end: int = 10) -> List[Dict[str, Any]]:
        """搜索收藏文章"""
        try:
            likes = db.query(Like).filter(
                Like.title.contains(search_data) |
                Like.content.contains(search_data) |
                Like.digest.contains(search_data)
            ).order_by(Like.like_time.desc()).offset(start).limit(end - start).all()
            
            result = []
            for like in likes:
                like_data = {
                    'id': like.id,
                    'nickname': like.nickname,
                    'title': like.title,
                    'author': like.author,
                    'content_url': like.content_url,
                    'source_url': like.source_url,
                    'p_date': like.p_date,
                    'like_time': like.like_time,
                    'read_num': like.read_num,
                    'like_num': like.like_num,
                    'comment_num': like.comment_num,
                    'reward_num': like.reward_num,
                    'digest': like.digest,
                    'content': like.content
                }
                result.append(like_data)
            
            return result
        except Exception as e:
            logger.error(f"搜索收藏失败: {e}")
            return []
    
    def get_like_by_id(self, db: Session, like_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取收藏详情"""
        try:
            like = db.query(Like).filter(Like.id == like_id).first()
            if like:
                return {
                    'id': like.id,
                    'nickname': like.nickname,
                    'title': like.title,
                    'author': like.author,
                    'content_url': like.content_url,
                    'source_url': like.source_url,
                    'p_date': like.p_date,
                    'like_time': like.like_time,
                    'read_num': like.read_num,
                    'like_num': like.like_num,
                    'comment_num': like.comment_num,
                    'reward_num': like.reward_num,
                    'digest': like.digest,
                    'content': like.content
                }
            return None
        except Exception as e:
            logger.error(f"获取收藏详情失败: {e}")
            return None
    
    def bulk_export_likes(self, db: Session) -> List[Dict[str, Any]]:
        """批量导出收藏数据"""
        try:
            likes = db.query(Like).order_by(Like.like_time.desc()).all()
            
            result = []
            for like in likes:
                like_data = {
                    'nickname': like.nickname,
                    'title': like.title,
                    'author': like.author,
                    'content_url': like.content_url,
                    'source_url': like.source_url,
                    'p_date': like.p_date.isoformat() if like.p_date else None,
                    'like_time': like.like_time.isoformat() if like.like_time else None,
                    'read_num': like.read_num,
                    'like_num': like.like_num,
                    'comment_num': like.comment_num,
                    'reward_num': like.reward_num,
                    'digest': like.digest,
                    'content': like.content
                }
                result.append(like_data)
            
            return result
        except Exception as e:
            logger.error(f"导出收藏数据失败: {e}")
            return []


# 全局收藏服务实例
like_service = LikeService() 