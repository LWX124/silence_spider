"""
应用配置管理
"""

import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类"""
    
    # 基础配置
    PROJECT_NAME: str = "Silence Spider"
    VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # 服务器配置
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    ALLOWED_HOSTS: List[str] = Field(default=["*"], env="ALLOWED_HOSTS")
    
    # 数据库配置
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://user:password@localhost/silence_spider",
        env="DATABASE_URL"
    )
    
    # Redis配置
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    
    # Celery配置
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/1",
        env="CELERY_BROKER_URL"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/2",
        env="CELERY_RESULT_BACKEND"
    )
    
    # 安全配置
    SECRET_KEY: str = Field(
        default="your-secret-key-here",
        env="SECRET_KEY"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # 爬虫配置
    CRAWLER_DELAY: float = Field(default=1.0, env="CRAWLER_DELAY")
    CRAWLER_TIMEOUT: int = Field(default=30, env="CRAWLER_TIMEOUT")
    CRAWLER_RETRY_TIMES: int = Field(default=3, env="CRAWLER_RETRY_TIMES")
    
    # 代理配置
    PROXY_ENABLED: bool = Field(default=False, env="PROXY_ENABLED")
    PROXY_URL: Optional[str] = Field(default=None, env="PROXY_URL")
    PROXY_USERNAME: Optional[str] = Field(default=None, env="PROXY_USERNAME")
    PROXY_PASSWORD: Optional[str] = Field(default=None, env="PROXY_PASSWORD")
    
    # 文件存储配置
    UPLOAD_DIR: str = Field(default="./uploads", env="UPLOAD_DIR")
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    
    # 日志配置
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="./logs/app.log", env="LOG_FILE")
    
    # Elasticsearch配置
    ELASTICSEARCH_URL: str = Field(
        default="http://localhost:9200",
        env="ELASTICSEARCH_URL"
    )
    
    # 微信相关配置
    WECHAT_COOKIE_FILE: str = Field(
        default="./data/wechat_cookies.json",
        env="WECHAT_COOKIE_FILE"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()


# 确保必要的目录存在
def ensure_directories():
    """确保必要的目录存在"""
    directories = [
        settings.UPLOAD_DIR,
        os.path.dirname(settings.LOG_FILE),
        os.path.dirname(settings.WECHAT_COOKIE_FILE),
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


# 初始化时创建目录
ensure_directories() 