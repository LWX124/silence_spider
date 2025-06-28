"""
Silence Spider - 现代化微信爬虫系统
主入口文件
"""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.core.config import settings
from app.core.database import engine
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 Starting Silence Spider...")
    
    # 初始化数据库连接
    await engine.connect()
    logger.info("✅ Database connected")
    
    yield
    
    # 关闭时执行
    logger.info("🛑 Shutting down Silence Spider...")
    await engine.dispose()
    logger.info("✅ Database disconnected")


def create_application() -> FastAPI:
    """创建FastAPI应用实例"""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="现代化微信公众文章爬虫系统",
        version=settings.VERSION,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )
    
    # 添加中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # 注册路由
    app.include_router(api_router, prefix="/api/v1")
    
    # 静态文件服务
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    return app


app = create_application()


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Silence Spider API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning",
    ) 