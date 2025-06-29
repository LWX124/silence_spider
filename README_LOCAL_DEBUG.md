# Silence Spider 本地调试

这个项目已经配置好了本地调试环境，可以快速启动后端服务进行开发调试。

## 🚀 快速开始

### 方法一：使用简化脚本（推荐）

1. **启动依赖服务**

   ```bash
   # macOS/Linux
   ./start_deps.sh

   # Windows
   start_deps.bat
   ```

2. **启动后端服务**
   ```bash
   cd backend
   python start_dev.py
   ```

### 方法二：使用完整脚本

1. **启动依赖服务**

   ```bash
   # macOS/Linux
   ./start_deps.sh

   # Windows
   start_deps.bat
   ```

2. **启动后端服务**
   ```bash
   cd backend
   python debug_local.py
   ```

### 方法三：使用 VS Code 调试（推荐）

1. **启动依赖服务**

   ```bash
   # macOS/Linux
   ./start_deps.sh

   # Windows
   start_deps.bat
   ```

2. **在 VS Code 中启动调试**
   - 按 `F5` 或点击调试按钮
   - 选择 "FastAPI: 启动后端服务"
   - 服务将在调试模式下启动

## 📋 服务信息

启动成功后可以访问：

- **API 服务**: http://127.0.0.1:8000
- **API 文档**: http://127.0.0.1:8000/docs
- **健康检查**: http://127.0.0.1:8000/health

## 🔧 手动启动（如果自动脚本有问题）

### 1. 启动 Docker 依赖

```bash
docker-compose up -d postgres redis elasticsearch
```

### 2. 设置 Python 环境

```bash
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. 创建环境变量

```bash
# 在backend目录下创建.env文件
cat > .env << EOF
DEBUG=true
HOST=127.0.0.1
PORT=8000
DATABASE_URL=postgresql+asyncpg://spider_user:spider_password@localhost:5432/silence_spider
REDIS_URL=redis://localhost:6379/0
ELASTICSEARCH_URL=http://localhost:9200
SECRET_KEY=debug-secret-key
UPLOAD_DIR=./uploads
LOG_FILE=./logs/app.log
WECHAT_COOKIE_FILE=./data/wechat_cookies.json
EOF
```

### 4. 启动后端

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

## 🛠️ VS Code 配置

项目已预配置 VS Code 开发环境：

### 调试配置

- **FastAPI: 启动后端服务** - 带热重载的调试模式
- **FastAPI: 调试模式（无重载）** - 纯调试模式
- **FastAPI: 自定义端口** - 使用 8001 端口
- **Python: 直接运行 main.py** - 直接运行主文件

### 任务配置

- **启动依赖服务** - 启动 Docker 服务
- **安装 Python 依赖** - 安装 requirements.txt
- **数据库迁移** - 执行 alembic 迁移
- **代码格式化** - 使用 black 格式化
- **代码检查** - 使用 flake8 检查
- **运行测试** - 执行 pytest 测试

### 快捷键

- `F5` - 启动调试
- `Ctrl+Shift+P` - 打开命令面板
- `Ctrl+Shift+P` → "Tasks: Run Task" - 运行任务

## 📚 详细文档

更多详细信息请查看：[docs/local_debug.md](docs/local_debug.md)

## 🛑 停止服务

```bash
# 停止后端服务
Ctrl+C

# 停止Docker服务
docker-compose down
```

## 🔍 故障排除

### 常见问题

1. **端口被占用**

   ```bash
   # 使用其他端口
   python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
   ```

2. **数据库连接失败**

   ```bash
   # 检查Docker服务
   docker-compose ps
   ```

3. **依赖安装失败**

   ```bash
   # 升级pip
   pip install --upgrade pip
   # 重新安装
   pip install -r requirements.txt
   ```

4. **VS Code 调试不工作**
   - 确保选择了正确的 Python 解释器
   - 检查是否在 backend 目录下运行
   - 确保依赖服务已启动
