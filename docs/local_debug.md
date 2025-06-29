# 本地调试指南

本指南将帮助你设置 Silence Spider 后端的本地调试环境，无需启动完整的 Docker 服务。

## 前置要求

1. **Python 3.8+**
2. **Docker Desktop** (用于运行数据库等依赖服务)
3. **Git**

## 快速开始

### 方法一：使用自动化脚本（推荐）

1. **启动依赖服务**
   ```bash
   # macOS/Linux
   chmod +x start_deps.sh
   ./start_deps.sh
   
   # Windows
   start_deps.bat
   ```

2. **启动后端服务**
   ```bash
   cd backend
   python debug_local.py
   ```

### 方法二：手动设置

1. **创建Python虚拟环境**
   ```bash
   cd backend
   python -m venv venv
   
   # macOS/Linux
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动依赖服务**
   ```bash
   # 在项目根目录
   docker-compose up -d postgres redis elasticsearch
   ```

4. **创建环境变量文件**
   ```bash
   cd backend
   # 复制并修改 .env.example 或创建新的 .env 文件
   ```

5. **执行数据库迁移**
   ```bash
   alembic upgrade head
   ```

6. **启动后端服务**
   ```bash
   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

## 环境配置

### 环境变量 (.env)

```env
# 本地调试环境配置
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
```

### 数据库连接信息

- **主机**: localhost
- **端口**: 5432
- **数据库**: silence_spider
- **用户名**: spider_user
- **密码**: spider_password

## 服务访问

启动成功后，你可以访问以下地址：

- **API服务**: http://127.0.0.1:8000
- **API文档**: http://127.0.0.1:8000/docs
- **健康检查**: http://127.0.0.1:8000/health

## 调试功能

### 热重载
服务启动时启用了 `--reload` 参数，代码修改后会自动重启。

### 日志
- 应用日志: `backend/logs/app.log`
- 控制台输出: 实时显示请求和错误信息

### 数据库管理
```bash
# 创建新的迁移
alembic revision --autogenerate -m "描述"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## 常见问题

### 1. 端口被占用
如果8000端口被占用，可以修改端口：
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

### 2. 数据库连接失败
检查Docker服务是否正常运行：
```bash
docker-compose ps
```

### 3. 依赖安装失败
尝试升级pip：
```bash
pip install --upgrade pip
```

### 4. 权限问题
确保脚本有执行权限：
```bash
chmod +x start_deps.sh
chmod +x backend/debug_local.py
```

## 开发工具

### VS Code 配置

创建 `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app",
                "--host", "127.0.0.1",
                "--port", "8000",
                "--reload"
            ],
            "cwd": "${workspaceFolder}/backend",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/backend"
            }
        }
    ]
}
```

### PyCharm 配置

1. 创建新的运行配置
2. 脚本路径: `backend/main.py`
3. 工作目录: `backend`
4. 环境变量: 添加 `.env` 文件中的变量

## 停止服务

```bash
# 停止后端服务
Ctrl+C

# 停止Docker服务
docker-compose down
```

## 清理环境

```bash
# 删除虚拟环境
rm -rf backend/venv

# 删除日志和上传文件
rm -rf backend/logs/*
rm -rf backend/uploads/*

# 停止并删除Docker容器
docker-compose down -v
``` 