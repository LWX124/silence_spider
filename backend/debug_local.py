#!/usr/bin/env python3
"""
本地调试脚本 - 启动Silence Spider后端服务
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(command, description, check=True):
    """运行命令并显示输出"""
    print(f"\n🔄 {description}")
    print(f"执行命令: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print("输出:", result.stdout)
        if result.stderr:
            print("错误:", result.stderr)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        return False

def check_service_running(service_name, port):
    """检查服务是否正在运行"""
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0
    except:
        return False

def main():
    print("🚀 Silence Spider 本地调试环境启动")
    print("=" * 50)
    
    # 检查当前目录
    current_dir = Path.cwd()
    if not (current_dir / "main.py").exists():
        print("❌ 请在backend目录下运行此脚本")
        sys.exit(1)
    
    # 1. 检查虚拟环境
    print("\n📋 检查Python虚拟环境...")
    if not os.environ.get('VIRTUAL_ENV'):
        print("⚠️  未检测到虚拟环境，建议创建虚拟环境:")
        print("   python -m venv venv")
        print("   source venv/bin/activate  # macOS/Linux")
        print("   venv\\Scripts\\activate     # Windows")
        response = input("是否继续？(y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # 2. 安装依赖
    print("\n📦 安装Python依赖...")
    if not run_command("pip install -r requirements.txt", "安装依赖包"):
        print("❌ 依赖安装失败")
        sys.exit(1)
    
    # 3. 检查Docker服务
    print("\n🐳 检查Docker服务状态...")
    
    services = [
        ("PostgreSQL", 5432),
        ("Redis", 6379),
        ("Elasticsearch", 9200)
    ]
    
    docker_running = True
    for service_name, port in services:
        if check_service_running(service_name, port):
            print(f"✅ {service_name} 正在运行 (端口 {port})")
        else:
            print(f"❌ {service_name} 未运行 (端口 {port})")
            docker_running = False
    
    if not docker_running:
        print("\n⚠️  检测到依赖服务未运行")
        print("请启动Docker服务:")
        print("   docker-compose up -d postgres redis elasticsearch")
        
        response = input("是否现在启动Docker服务？(y/n): ")
        if response.lower() == 'y':
            if not run_command("docker-compose up -d postgres redis elasticsearch", "启动Docker服务"):
                print("❌ Docker服务启动失败")
                sys.exit(1)
            
            print("⏳ 等待服务启动...")
            time.sleep(10)
        else:
            print("❌ 无法继续，需要依赖服务运行")
            sys.exit(1)
    
    # 4. 创建环境变量文件
    print("\n⚙️  创建环境变量文件...")
    env_content = """# 本地调试环境配置
DEBUG=true
HOST=127.0.0.1
PORT=8000

# 数据库配置
DATABASE_URL=postgresql+asyncpg://spider_user:spider_password@localhost:5432/silence_spider

# Redis配置
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# Elasticsearch配置
ELASTICSEARCH_URL=http://localhost:9200

# 安全配置
SECRET_KEY=debug-secret-key-change-in-production

# 文件存储配置
UPLOAD_DIR=./uploads
LOG_FILE=./logs/app.log

# 微信相关配置
WECHAT_COOKIE_FILE=./data/wechat_cookies.json
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    print("✅ 环境变量文件已创建")
    
    # 5. 创建必要目录
    print("\n📁 创建必要目录...")
    directories = ["uploads", "logs", "data"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ 目录 {directory} 已创建")
    
    # 6. 数据库迁移
    print("\n🗄️  执行数据库迁移...")
    
    # 检查alembic是否已初始化
    if not (Path("alembic.ini")).exists():
        print("⚠️  Alembic未初始化，正在初始化...")
        if run_command("alembic init alembic", "初始化Alembic"):
            # 修改alembic.ini中的数据库URL
            with open("alembic.ini", "r", encoding="utf-8") as f:
                content = f.read()
            
            content = content.replace(
                "sqlalchemy.url = driver://user:pass@localhost/dbname",
                "sqlalchemy.url = postgresql+asyncpg://spider_user:spider_password@localhost:5432/silence_spider"
            )
            
            with open("alembic.ini", "w", encoding="utf-8") as f:
                f.write(content)
            
            # 修改env.py文件
            env_py_path = Path("alembic/env.py")
            if env_py_path.exists():
                with open(env_py_path, "r", encoding="utf-8") as f:
                    env_content = f.read()
                
                # 添加导入
                import_section = """import os
from dotenv import load_dotenv

load_dotenv()

"""
                env_content = import_section + env_content
                
                # 修改config部分
                env_content = env_content.replace(
                    "config.set_main_option('sqlalchemy.url', url)",
                    """# 从环境变量获取数据库URL
    database_url = os.getenv('DATABASE_URL', url)
    config.set_main_option('sqlalchemy.url', database_url)"""
                )
                
                with open(env_py_path, "w", encoding="utf-8") as f:
                    f.write(env_content)
            
            print("✅ Alembic初始化完成")
        else:
            print("❌ Alembic初始化失败")
            sys.exit(1)
    
    # 执行迁移
    if not run_command("alembic upgrade head", "执行数据库迁移", check=False):
        print("⚠️  数据库迁移失败，可能是首次运行")
        if run_command("alembic revision --autogenerate -m 'Initial migration'", "创建初始迁移"):
            run_command("alembic upgrade head", "执行数据库迁移")
    
    # 7. 启动后端服务
    print("\n🚀 启动后端服务...")
    print("服务将在 http://127.0.0.1:8000 启动")
    print("API文档: http://127.0.0.1:8000/docs")
    print("按 Ctrl+C 停止服务")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 服务已停止")
    except Exception as e:
        print(f"\n❌ 服务启动失败: {e}")

if __name__ == "__main__":
    main() 