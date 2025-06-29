"""
微信公众号连接服务
实现参数管理、爬虫执行等功能
"""
import json
import re
import logging
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.article import Article
from app.models.proxy import Proxy
from app.services.proxy_service import proxy_service
from app.services.websocket_service import WebSocketService
import aiohttp
import hashlib

logger = logging.getLogger(__name__)


class WeChatService:
    """微信公众号服务类"""
    
    def __init__(self):
        self.request_data = {}
        self.current_wxuin = None
        self.current_nickname = None
    
    async def start_proxy_server(self):
        """启动代理服务器"""
        try:
            await proxy_service.start_proxy()
            logger.info("代理服务器启动成功")
            return True
        except Exception as e:
            logger.error(f"代理服务器启动失败: {e}")
            return False
    
    def get_proxy_info(self) -> Dict[str, Any]:
        """获取代理服务器信息"""
        import socket
        try:
            # 获取本机IP
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return {
                'ip': ip,
                'port': 8080,
                'status': 'running' if proxy_service.is_proxy_running() else 'stopped'
            }
        except Exception as e:
            logger.error(f"获取代理信息失败: {e}")
            return {'ip': 'unknown', 'port': 8080, 'status': 'error'}
    
    def save_request_data(self, wxuin: str, key: str, data: Dict[str, Any]):
        """保存请求参数"""
        try:
            key_name = f"{wxuin}.{key}.req"
            self.request_data[key_name] = {
                'data': data,
                'timestamp': datetime.now().timestamp(),
                'wxuin': wxuin,
                'key': key
            }
            logger.info(f"保存请求参数: {key_name}")
            return True
        except Exception as e:
            logger.error(f"保存请求参数失败: {e}")
            return False
    
    def get_request_data(self, wxuin: str, key: str) -> Optional[Dict[str, Any]]:
        """获取请求参数"""
        key_name = f"{wxuin}.{key}.req"
        return self.request_data.get(key_name)
    
    def get_all_request_data(self) -> List[Dict[str, Any]]:
        """获取所有请求参数"""
        result = []
        for key_name, data in self.request_data.items():
            result.append({
                'key': key_name,
                'wxuin': data['wxuin'],
                'type': data['key'],
                'timestamp': data['timestamp'],
                'data': data['data']
            })
        return result
    
    def delete_request_data(self, wxuin: str = None, key: str = None):
        """删除请求参数"""
        if wxuin and key:
            # 删除特定参数
            key_name = f"{wxuin}.{key}.req"
            if key_name in self.request_data:
                del self.request_data[key_name]
                logger.info(f"删除请求参数: {key_name}")
        elif wxuin:
            # 删除特定微信的所有参数
            keys_to_delete = [k for k in self.request_data.keys() if k.startswith(f"{wxuin}.")]
            for key in keys_to_delete:
                del self.request_data[key]
            logger.info(f"删除微信 {wxuin} 的所有参数")
        else:
            # 删除所有参数
            self.request_data.clear()
            logger.info("删除所有请求参数")
    
    async def crawl_article_list(self, nickname: str, offset: int = 0) -> Optional[Dict[str, Any]]:
        """爬取文章列表"""
        try:
            # 获取请求参数
            wx_req_data = self._get_wx_req_data_by_nickname(nickname)
            if not wx_req_data or 'load_more' not in wx_req_data:
                logger.error(f"未找到公众号 {nickname} 的请求参数")
                return None
            
            # 构建请求
            req_data = wx_req_data['load_more']['data']
            url = req_data['url']
            headers = req_data['requestOptions']['headers']
            
            # 修改offset参数
            url = re.sub(r'offset=\d+', f'offset={offset}', url)
            
            # 发送请求
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # 检查响应状态
                        if data.get('errmsg') == 'ok':
                            # 解析文章列表
                            articles = self._parse_article_list(data, nickname)
                            
                            # 发送进度更新
                            await WebSocketService.send_progress({
                                'type': 'article_list',
                                'nickname': nickname,
                                'count': len(articles),
                                'offset': offset
                            })
                            
                            return {
                                'articles': articles,
                                'can_continue': data.get('can_msg_continue', False),
                                'next_offset': data.get('next_offset', 0)
                            }
                        else:
                            logger.error(f"获取文章列表失败: {data}")
                            return None
                    else:
                        logger.error(f"请求失败: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"爬取文章列表失败: {e}")
            return None
    
    async def crawl_article_content(self, article_url: str, nickname: str) -> Optional[Dict[str, Any]]:
        """爬取文章内容"""
        try:
            # 获取请求参数
            wx_req_data = self._get_wx_req_data_by_nickname(nickname)
            if not wx_req_data or 'content' not in wx_req_data:
                logger.error(f"未找到公众号 {nickname} 的内容请求参数")
                return None
            
            # 构建请求
            req_data = wx_req_data['content']['data']
            headers = req_data['requestOptions']['headers']
            
            # 发送请求
            async with aiohttp.ClientSession() as session:
                async with session.get(article_url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # 解析文章内容
                        article_data = self._parse_article_content(content, article_url)
                        
                        return article_data
                    else:
                        logger.error(f"获取文章内容失败: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"爬取文章内容失败: {e}")
            return None
    
    async def crawl_reading_data(self, article_url: str, nickname: str) -> Optional[Dict[str, Any]]:
        """爬取阅读数据"""
        try:
            # 获取请求参数
            wx_req_data = self._get_wx_req_data_by_nickname(nickname)
            if not wx_req_data or 'getappmsgext' not in wx_req_data:
                logger.error(f"未找到公众号 {nickname} 的阅读数据请求参数")
                return None
            
            # 构建请求
            req_data = wx_req_data['getappmsgext']['data']
            url = req_data['url']
            headers = req_data['requestOptions']['headers']
            
            # 修改URL参数
            url = re.sub(r'__biz=[^&]+', f'__biz={self._extract_biz_from_url(article_url)}', url)
            
            # 发送请求
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        return {
                            'read_num': data.get('appmsgstat', {}).get('read_num', 0),
                            'like_num': data.get('appmsgstat', {}).get('like_num', 0),
                            'reward_num': data.get('reward_total_count', 0),
                            'comment_num': data.get('comment_count', 0)
                        }
                    else:
                        logger.error(f"获取阅读数据失败: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"爬取阅读数据失败: {e}")
            return None
    
    def _get_wx_req_data_by_nickname(self, nickname: str) -> Optional[Dict[str, Any]]:
        """根据公众号名称获取微信请求参数"""
        # 这里需要根据实际存储方式实现
        # 暂时返回空，需要根据数据库或缓存中的实际数据实现
        return None
    
    def _parse_article_list(self, data: Dict[str, Any], nickname: str) -> List[Dict[str, Any]]:
        """解析文章列表"""
        articles = []
        
        try:
            # 解析general_msg_list
            msg_list = data.get('general_msg_list', '[]')
            msg_list = msg_list.replace(r"\/", "/")
            msg_data = json.loads(msg_list)
            
            for msg in msg_data.get('list', []):
                p_date = msg.get("comm_msg_info", {}).get("datetime")
                msg_info = msg.get("app_msg_ext_info")
                
                if msg_info:
                    # 主文章
                    article = self._extract_article_info(msg_info, nickname, p_date, 10)
                    if article:
                        articles.append(article)
                    
                    # 副文章
                    multi_msg_info = msg_info.get("multi_app_msg_item_list", [])
                    for i, msg_item in enumerate(multi_msg_info):
                        article = self._extract_article_info(msg_item, nickname, p_date, 11 + i)
                        if article:
                            articles.append(article)
                            
        except Exception as e:
            logger.error(f"解析文章列表失败: {e}")
        
        return articles
    
    def _extract_article_info(self, msg_info: Dict[str, Any], nickname: str, p_date: int, mov: int) -> Optional[Dict[str, Any]]:
        """提取文章信息"""
        try:
            title = msg_info.get('title', '').strip()
            if not title:
                return None
            
            article = {
                'title': title,
                'author': msg_info.get('author', ''),
                'content_url': msg_info.get('content_url', ''),
                'source_url': msg_info.get('source_url', ''),
                'digest': msg_info.get('digest', ''),
                'cover': msg_info.get('cover', ''),
                'nickname': nickname,
                'mov': mov,
                'p_date': datetime.fromtimestamp(p_date) if p_date else None,
                'id': self._generate_article_id(msg_info.get('content_url', ''))
            }
            
            return article
            
        except Exception as e:
            logger.error(f"提取文章信息失败: {e}")
            return None
    
    def _parse_article_content(self, content: str, url: str) -> Dict[str, Any]:
        """解析文章内容"""
        # 这里需要实现HTML解析逻辑
        # 暂时返回基础信息
        return {
            'url': url,
            'content': content,
            'parsed_at': datetime.now()
        }
    
    def _extract_biz_from_url(self, url: str) -> str:
        """从文章URL中提取__biz参数"""
        match = re.search(r'__biz=([^&]+)', url)
        return match.group(1) if match else ''
    
    def _generate_article_id(self, url: str) -> str:
        """生成文章ID"""
        return hashlib.md5(url.encode()).hexdigest()


# 全局微信服务实例
wechat_service = WeChatService() 