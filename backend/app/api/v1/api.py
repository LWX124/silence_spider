"""
API v1 路由注册
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, export, likes, search, websocket, accounts

api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["公众号管理"])
api_router.include_router(export.router, prefix="/export", tags=["导出"])
api_router.include_router(likes.router, prefix="/likes", tags=["点赞"])
api_router.include_router(search.router, prefix="/search", tags=["搜索"])
api_router.include_router(websocket.router, prefix="/ws", tags=["WebSocket"]) 