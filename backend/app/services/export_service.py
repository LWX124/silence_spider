"""
导出服务
支持Excel等格式的数据导出
"""
import logging
import os
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.article import Article
from app.services.like_service import like_service

logger = logging.getLogger(__name__)


class ExportService:
    """导出服务类"""
    
    def __init__(self, output_folder: str = "exports"):
        self.output_folder = output_folder
        self._ensure_output_folder()
    
    def _ensure_output_folder(self):
        """确保输出文件夹存在"""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            logger.info(f"创建输出文件夹: {self.output_folder}")
    
    def export_articles_to_excel(self, db: Session, nickname: str = None) -> Optional[str]:
        """导出文章到Excel"""
        try:
            # 查询文章数据
            query = db.query(Article)
            if nickname:
                query = query.filter(Article.nickname == nickname)
            
            articles = query.order_by(Article.p_date.desc()).all()
            
            if not articles:
                logger.warning(f"没有找到文章数据: {nickname}")
                return None
            
            # 准备数据
            data = []
            for article in articles:
                row = {
                    "编号": len(data) + 1,
                    "阅读": article.read_num if article.read_num is not None else '-',
                    "点赞": article.like_num if article.like_num is not None else '-',
                    "赞赏": article.reward_num if article.reward_num is not None else '-',
                    "评论": article.comment_num if article.comment_num is not None else '-',
                    "位置": article.mov if article.mov is not None else '-',
                    "发文时间": article.p_date.strftime('%Y-%m-%d %H:%M:%S') if article.p_date else '-',
                    "作者": article.author or '-',
                    "标题": article.title or '-',
                    "链接": article.content_url or '-',
                    "原文链接": article.source_url or '-',
                    "摘要": article.digest or '-',
                    "收藏": "是" if article.like_folder else "否"
                }
                data.append(row)
            
            # 创建DataFrame
            df = pd.DataFrame(data)
            
            # 生成文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if nickname:
                filename = f"{nickname}_{timestamp}.xlsx"
            else:
                filename = f"all_articles_{timestamp}.xlsx"
            
            filepath = os.path.join(self.output_folder, filename)
            
            # 写入Excel
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                sheet_name = nickname or "全部文章"
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # 调整列宽
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            logger.info(f"Excel导出成功: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Excel导出失败: {e}")
            return None
    
    def export_likes_to_excel(self, db: Session) -> Optional[str]:
        """导出收藏到Excel"""
        try:
            # 获取收藏数据
            likes_data = like_service.bulk_export_likes(db)
            
            if not likes_data:
                logger.warning("没有找到收藏数据")
                return None
            
            # 准备数据
            data = []
            for like in likes_data:
                row = {
                    "编号": len(data) + 1,
                    "公众号": like['nickname'] or '-',
                    "标题": like['title'] or '-',
                    "作者": like['author'] or '-',
                    "发布时间": like['p_date'] or '-',
                    "收藏时间": like['like_time'] or '-',
                    "阅读数": like['read_num'] if like['read_num'] is not None else '-',
                    "点赞数": like['like_num'] if like['like_num'] is not None else '-',
                    "评论数": like['comment_num'] if like['comment_num'] is not None else '-',
                    "赞赏数": like['reward_num'] if like['reward_num'] is not None else '-',
                    "文章链接": like['content_url'] or '-',
                    "原文链接": like['source_url'] or '-',
                    "摘要": like['digest'] or '-'
                }
                data.append(row)
            
            # 创建DataFrame
            df = pd.DataFrame(data)
            
            # 生成文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"likes_{timestamp}.xlsx"
            filepath = os.path.join(self.output_folder, filename)
            
            # 写入Excel
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name="收藏文章", index=False)
                
                # 调整列宽
                worksheet = writer.sheets["收藏文章"]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            logger.info(f"收藏Excel导出成功: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"收藏Excel导出失败: {e}")
            return None
    
    def export_search_results_to_excel(self, search_results: List[Dict[str, Any]], search_keyword: str) -> Optional[str]:
        """导出搜索结果到Excel"""
        try:
            if not search_results:
                logger.warning("没有搜索结果数据")
                return None
            
            # 准备数据
            data = []
            for result in search_results:
                row = {
                    "编号": len(data) + 1,
                    "公众号": result.get('nickname', '-'),
                    "标题": result.get('title', '-'),
                    "作者": result.get('author', '-'),
                    "发布时间": result.get('p_date', '-'),
                    "阅读数": result.get('read_num', '-'),
                    "点赞数": result.get('like_num', '-'),
                    "评论数": result.get('comment_num', '-'),
                    "赞赏数": result.get('reward_num', '-'),
                    "文章链接": result.get('content_url', '-'),
                    "原文链接": result.get('source_url', '-'),
                    "摘要": result.get('digest', '-'),
                    "相关度": f"{result.get('score', 0):.2f}"
                }
                data.append(row)
            
            # 创建DataFrame
            df = pd.DataFrame(data)
            
            # 生成文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_keyword = "".join(c for c in search_keyword if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"search_{safe_keyword}_{timestamp}.xlsx"
            filepath = os.path.join(self.output_folder, filename)
            
            # 写入Excel
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name="搜索结果", index=False)
                
                # 调整列宽
                worksheet = writer.sheets["搜索结果"]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            logger.info(f"搜索结果Excel导出成功: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"搜索结果Excel导出失败: {e}")
            return None
    
    def get_export_files(self) -> List[Dict[str, Any]]:
        """获取导出文件列表"""
        try:
            files = []
            if os.path.exists(self.output_folder):
                for filename in os.listdir(self.output_folder):
                    if filename.endswith('.xlsx'):
                        filepath = os.path.join(self.output_folder, filename)
                        stat = os.stat(filepath)
                        files.append({
                            'filename': filename,
                            'filepath': filepath,
                            'size': stat.st_size,
                            'created_time': datetime.fromtimestamp(stat.st_ctime),
                            'modified_time': datetime.fromtimestamp(stat.st_mtime)
                        })
            
            # 按修改时间排序
            files.sort(key=lambda x: x['modified_time'], reverse=True)
            return files
            
        except Exception as e:
            logger.error(f"获取导出文件列表失败: {e}")
            return []
    
    def delete_export_file(self, filename: str) -> bool:
        """删除导出文件"""
        try:
            filepath = os.path.join(self.output_folder, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"删除导出文件: {filepath}")
                return True
            return False
        except Exception as e:
            logger.error(f"删除导出文件失败: {e}")
            return False


# 全局导出服务实例
export_service = ExportService() 