"""
Mac 版微信数据获取服务
尝试从 Mac 版微信获取数据
"""
import os
import sqlite3
import logging
import shutil
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class MacWeChatService:
    """Mac 版微信服务类"""
    
    def __init__(self):
        self.wechat_data_path = self._get_wechat_data_path()
        self.backup_path = None
    
    def _get_wechat_data_path(self) -> str:
        """获取微信数据路径"""
        # Mac 版微信数据通常存储在以下位置
        home = os.path.expanduser("~")
        possible_paths = [
            f"{home}/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat",
            f"{home}/Library/Application Support/WeChat",
            f"{home}/Library/Containers/com.tencent.xinWeChat/Data/Documents"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"找到微信数据路径: {path}")
                return path
        
        logger.warning("未找到微信数据路径")
        return ""
    
    def create_backup(self) -> bool:
        """创建微信数据备份"""
        try:
            if not self.wechat_data_path:
                logger.error("微信数据路径不存在")
                return False
            
            # 创建备份目录
            backup_dir = f"/tmp/wechat_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(backup_dir, exist_ok=True)
            
            # 复制数据文件
            shutil.copytree(self.wechat_data_path, f"{backup_dir}/wechat_data")
            self.backup_path = backup_dir
            
            logger.info(f"微信数据备份完成: {backup_dir}")
            return True
            
        except Exception as e:
            logger.error(f"创建备份失败: {e}")
            return False
    
    def find_database_files(self) -> List[str]:
        """查找数据库文件"""
        db_files = []
        
        if not self.backup_path:
            logger.error("请先创建备份")
            return db_files
        
        # 常见的数据库文件扩展名
        db_extensions = ['.db', '.sqlite', '.sqlite3']
        
        for root, dirs, files in os.walk(self.backup_path):
            for file in files:
                if any(file.endswith(ext) for ext in db_extensions):
                    db_files.append(os.path.join(root, file))
        
        logger.info(f"找到 {len(db_files)} 个数据库文件")
        return db_files
    
    def analyze_database(self, db_path: str) -> Dict[str, Any]:
        """分析数据库结构"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 获取所有表名
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            result = {
                'path': db_path,
                'tables': [],
                'size': os.path.getsize(db_path)
            }
            
            for table in tables:
                table_name = table[0]
                try:
                    # 获取表结构
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()
                    
                    # 获取记录数
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                    count = cursor.fetchone()[0]
                    
                    result['tables'].append({
                        'name': table_name,
                        'columns': [col[1] for col in columns],
                        'count': count
                    })
                except Exception as e:
                    logger.warning(f"分析表 {table_name} 失败: {e}")
            
            conn.close()
            return result
            
        except Exception as e:
            logger.error(f"分析数据库失败: {e}")
            return {'path': db_path, 'error': str(e)}
    
    def extract_messages(self, db_path: str, limit: int = 100) -> List[Dict[str, Any]]:
        """提取消息数据"""
        messages = []
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 尝试常见的消息表名
            possible_tables = ['message', 'msg', 'chat', 'conversation', 'wechat_message']
            
            for table_name in possible_tables:
                try:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
                    rows = cursor.fetchall()
                    
                    if rows:
                        # 获取列名
                        cursor.execute(f"PRAGMA table_info({table_name});")
                        columns = [col[1] for col in cursor.fetchall()]
                        
                        for row in rows:
                            message = dict(zip(columns, row))
                            message['table'] = table_name
                            messages.append(message)
                        
                        logger.info(f"从表 {table_name} 提取了 {len(rows)} 条消息")
                        break
                        
                except Exception as e:
                    continue
            
            conn.close()
            
        except Exception as e:
            logger.error(f"提取消息失败: {e}")
        
        return messages
    
    def extract_contacts(self, db_path: str) -> List[Dict[str, Any]]:
        """提取联系人数据"""
        contacts = []
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 尝试常见的联系人表名
            possible_tables = ['contact', 'friend', 'user', 'wechat_contact']
            
            for table_name in possible_tables:
                try:
                    cursor.execute(f"SELECT * FROM {table_name};")
                    rows = cursor.fetchall()
                    
                    if rows:
                        # 获取列名
                        cursor.execute(f"PRAGMA table_info({table_name});")
                        columns = [col[1] for col in cursor.fetchall()]
                        
                        for row in rows:
                            contact = dict(zip(columns, row))
                            contact['table'] = table_name
                            contacts.append(contact)
                        
                        logger.info(f"从表 {table_name} 提取了 {len(rows)} 个联系人")
                        break
                        
                except Exception as e:
                    continue
            
            conn.close()
            
        except Exception as e:
            logger.error(f"提取联系人失败: {e}")
        
        return contacts
    
    def extract_media_files(self) -> List[str]:
        """提取媒体文件路径"""
        media_files = []
        
        if not self.backup_path:
            return media_files
        
        # 常见的媒体文件扩展名
        media_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi', '.wav', '.mp3']
        
        for root, dirs, files in os.walk(self.backup_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in media_extensions):
                    media_files.append(os.path.join(root, file))
        
        logger.info(f"找到 {len(media_files)} 个媒体文件")
        return media_files
    
    def cleanup_backup(self):
        """清理备份文件"""
        if self.backup_path and os.path.exists(self.backup_path):
            try:
                shutil.rmtree(self.backup_path)
                logger.info(f"清理备份: {self.backup_path}")
                self.backup_path = None
            except Exception as e:
                logger.error(f"清理备份失败: {e}")
    
    def get_wechat_info(self) -> Dict[str, Any]:
        """获取微信基本信息"""
        info = {
            'data_path': self.wechat_data_path,
            'backup_path': self.backup_path,
            'exists': bool(self.wechat_data_path),
            'backup_exists': bool(self.backup_path)
        }
        
        if self.wechat_data_path:
            info['data_size'] = self._get_directory_size(self.wechat_data_path)
        
        return info
    
    def _get_directory_size(self, path: str) -> int:
        """获取目录大小"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
        except Exception as e:
            logger.error(f"计算目录大小失败: {e}")
        
        return total_size


# 全局 Mac 微信服务实例
mac_wechat_service = MacWeChatService() 