#!/usr/bin/env python3
"""
简化的开发启动脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 启动 Silence Spider 开发环境")
    
    # 检查当前目录
    if not Path("main.py").exists():
        print("❌ 请在backend目录下运行此脚本")
        sys.exit(1)
    
    # 创建.env文件
    env_content = """DEBUG=true
HOST=127.0.0.1
PORT=8000
DATABASE_URL=postgresql+asyncpg://spider_user:spider_password@localhost:5432/silence_spider
REDIS_URL=redis://localhost:6379/0
ELASTICSEARCH_URL=http://localhost:9200
SECRET_KEY=debug-secret-key
UPLOAD_DIR=./uploads
LOG_FILE=./logs/app.log
WECHAT_COOKIE_FILE=./data/wechat_cookies.json
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    # 创建目录
    for dir_name in ["uploads", "logs", "data"]:
        Path(dir_name).mkdir(exist_ok=True)
    
    # 启动服务
    print("✅ 环境配置完成")
    print("🌐 服务地址: http://127.0.0.1:8000")
    print("📚 API文档: http://127.0.0.1:8000/docs")
    
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000", 
        "--reload"
    ])

if __name__ == "__main__":
    main() 