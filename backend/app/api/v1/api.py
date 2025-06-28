"""
API v1 路由注册
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, accounts, articles, tasks, proxies, crawler

api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["公众号"])
api_router.include_router(articles.router, prefix="/articles", tags=["文章"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["任务"])
api_router.include_router(proxies.router, prefix="/proxies", tags=["代理"])
api_router.include_router(crawler.router, prefix="/crawler", tags=["爬虫"]) 