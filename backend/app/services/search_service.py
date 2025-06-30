"""
搜索服务
集成Elasticsearch提供全文搜索功能
"""
import logging
from typing import Dict, List, Any, Optional
from elasticsearch import Elasticsearch, NotFoundError
from elasticsearch.exceptions import RequestError
from datetime import datetime

logger = logging.getLogger(__name__)


class SearchService:
    """搜索服务类"""
    
    def __init__(self, es_host: str = "localhost", es_port: int = 9200):
        self.es = Elasticsearch([{'host': es_host, 'port': es_port, 'scheme': 'http'}])
        self.index_prefix = "gzh_"
    
    def create_index(self, nickname: str) -> bool:
        """为公众号创建索引"""
        try:
            index_name = f"{self.index_prefix}{nickname}"
            if not self.es.indices.exists(index=index_name):
                # 创建索引映射
                mappings = {
                    "properties": {
                        "title": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "digest": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "content": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "author": {
                            "type": "keyword"
                        },
                        "nickname": {
                            "type": "keyword"
                        },
                        "p_date": {
                            "type": "date"
                        },
                        "content_url": {
                            "type": "keyword"
                        },
                        "read_num": {
                            "type": "integer"
                        },
                        "like_num": {
                            "type": "integer"
                        },
                        "comment_num": {
                            "type": "integer"
                        },
                        "reward_num": {
                            "type": "integer"
                        }
                    }
                }
                self.es.indices.create(index=index_name, mappings=mappings)
                logger.info(f"创建索引: {index_name}")
                return True
            return True
        except Exception as e:
            logger.error(f"创建索引失败: {e}")
            return False
    
    def index_article(self, nickname: str, article_data: Dict[str, Any]) -> bool:
        """索引文章数据"""
        try:
            index_name = f"{self.index_prefix}{nickname}"
            doc_id = article_data.get('content_url', '')
            doc = {
                'title': article_data.get('title', ''),
                'digest': article_data.get('digest', ''),
                'content': article_data.get('content', ''),
                'author': article_data.get('author', ''),
                'nickname': nickname,
                'p_date': article_data.get('p_date'),
                'content_url': article_data.get('content_url', ''),
                'read_num': article_data.get('read_num', 0),
                'like_num': article_data.get('like_num', 0),
                'comment_num': article_data.get('comment_num', 0),
                'reward_num': article_data.get('reward_num', 0),
                'indexed_at': datetime.now()
            }
            self.es.index(index=index_name, id=doc_id, document=doc)
            return True
        except Exception as e:
            logger.error(f"索引文章失败: {e}")
            return False
    
    def search_articles(self, 
                       search_data: str, 
                       gzhs: List[str] = None, 
                       fields: List[str] = None,
                       _from: int = 0, 
                       _size: int = 10) -> Dict[str, Any]:
        """搜索文章"""
        try:
            if gzhs is None:
                gzhs = []
            if fields is None:
                fields = []
            if gzhs and gzhs != ['全部']:
                indices = [f"{self.index_prefix}{gzh}" for gzh in gzhs]
            else:
                indices = f"{self.index_prefix}*"
            if not fields or '全部' in fields:
                fields = ['title', 'digest', 'content']
            should_clauses = []
            for field in fields:
                should_clauses.append({
                    "match": {
                        field: {
                            "query": search_data,
                            "boost": 2.0 if field == 'title' else 1.0
                        }
                    }
                })
            query = {
                "bool": {
                    "should": should_clauses,
                    "minimum_should_match": 1
                }
            }
            response = self.es.search(
                index=indices,
                query=query,
                highlight={
                    "fields": {
                        "title": {},
                        "digest": {},
                        "content": {"fragment_size": 200}
                    }
                },
                sort=[
                    {"_score": {"order": "desc"}},
                    {"p_date": {"order": "desc"}}
                ],
                from_=_from,
                size=_size
            )
            results = []
            for hit in response['hits']['hits']:
                result = hit['_source']
                result['score'] = hit['_score']
                result['highlights'] = hit.get('highlight', {})
                results.append(result)
            return {
                'total': response['hits']['total']['value'],
                'results': results,
                'took': response['took']
            }
        except Exception as e:
            logger.error(f"搜索失败: {e}")
            return {'total': 0, 'results': [], 'error': str(e)}
    
    def get_index_info(self) -> List[Dict[str, Any]]:
        """获取所有索引信息"""
        try:
            indices = self.es.indices.get(index=f"{self.index_prefix}*")
            index_info = []
            
            for index_name, index_data in indices.items():
                nickname = index_name.replace(self.index_prefix, '')
                doc_count = index_data['mappings'].get('_doc', {}).get('properties', {})
                
                # 获取文档数量
                try:
                    count_response = self.es.count(index=index_name)
                    doc_count = count_response['count']
                except:
                    doc_count = 0
                
                index_info.append({
                    'nickname': nickname,
                    'doc_count': doc_count,
                    'index_name': index_name
                })
            
            return index_info
        except Exception as e:
            logger.error(f"获取索引信息失败: {e}")
            return []
    
    def delete_index(self, nickname: str) -> bool:
        """删除索引"""
        try:
            index_name = f"{self.index_prefix}{nickname}"
            if self.es.indices.exists(index=index_name):
                self.es.indices.delete(index=index_name)
                logger.info(f"删除索引: {index_name}")
                return True
            return False
        except Exception as e:
            logger.error(f"删除索引失败: {e}")
            return False
    
    def bulk_index_articles(self, nickname: str, articles: List[Dict[str, Any]]) -> bool:
        """批量索引文章"""
        try:
            index_name = f"{self.index_prefix}{nickname}"
            actions = []
            
            for article in articles:
                doc_id = article.get('content_url', '')
                action = {
                    "_index": index_name,
                    "_id": doc_id,
                    "_source": {
                        'title': article.get('title', ''),
                        'digest': article.get('digest', ''),
                        'content': article.get('content', ''),
                        'author': article.get('author', ''),
                        'nickname': nickname,
                        'p_date': article.get('p_date'),
                        'content_url': article.get('content_url', ''),
                        'read_num': article.get('read_num', 0),
                        'like_num': article.get('like_num', 0),
                        'comment_num': article.get('comment_num', 0),
                        'reward_num': article.get('reward_num', 0),
                        'indexed_at': datetime.now()
                    }
                }
                actions.append(action)
            
            if actions:
                from elasticsearch.helpers import bulk
                bulk(self.es, actions)
                logger.info(f"批量索引 {len(actions)} 篇文章到 {index_name}")
                return True
            
            return False
        except Exception as e:
            logger.error(f"批量索引失败: {e}")
            return False


# 全局搜索服务实例
search_service = SearchService() 