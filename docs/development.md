# Silence Spider 开发指南

## 项目概述

Silence Spider 是一个现代化的微信公众文章爬虫系统，采用前后端分离架构，使用最新的技术栈构建。

## 技术栈

### 后端技术栈
- **FastAPI**: 现代化的Python Web框架，支持异步处理
- **SQLAlchemy 2.0**: 最新的ORM框架，支持异步数据库操作
- **PostgreSQL**: 强大的关系型数据库
- **Redis**: 缓存和任务队列
- **Celery**: 分布式任务队列
- **Playwright**: 现代化的浏览器自动化
- **Pydantic**: 数据验证和序列化

### 前端技术栈
- **Vue 3**: 最新的Vue框架，使用Composition API
- **TypeScript**: 类型安全的JavaScript
- **Vite**: 现代化的构建工具
- **Element Plus**: Vue 3版本的Element UI
- **ECharts 5**: 数据可视化
- **Pinia**: Vue 3状态管理

## 项目结构

```
silence_spider/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模型
│   │   ├── services/       # 业务逻辑
│   │   ├── tasks/          # Celery任务
│   │   └── utils/          # 工具函数
│   ├── alembic/            # 数据库迁移
│   ├── requirements.txt    # Python依赖
│   └── main.py            # 启动文件
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── components/     # Vue组件
│   │   ├── views/          # 页面
│   │   ├── stores/         # Pinia状态
│   │   ├── router/         # 路由配置
│   │   └── utils/          # 工具函数
│   ├── package.json        # Node.js依赖
│   └── vite.config.ts      # Vite配置
├── docker/                 # Docker配置
├── docs/                   # 文档
└── README.md              # 项目说明
```

## 开发环境搭建

### 1. 环境要求
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 14+
- Redis 6+

### 2. 后端开发环境

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等信息

# 运行数据库迁移
alembic upgrade head

# 启动开发服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 前端开发环境

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 4. 使用Docker开发

```bash
# 启动所有服务
./start.sh

# 或者手动启动
docker-compose up -d

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 开发规范

### 1. 代码风格

#### Python (后端)
- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 使用 flake8 进行代码检查
- 使用 mypy 进行类型检查

```bash
# 格式化代码
black .
isort .

# 代码检查
flake8 .
mypy .
```

#### TypeScript (前端)
- 使用 ESLint 进行代码检查
- 使用 Prettier 进行代码格式化
- 使用 TypeScript 进行类型检查

```bash
# 代码检查
npm run lint

# 类型检查
npm run type-check
```

### 2. Git提交规范

使用 Conventional Commits 规范：

```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建过程或辅助工具的变动
```

### 3. 分支管理

- `main`: 主分支，用于生产环境
- `develop`: 开发分支
- `feature/*`: 功能分支
- `hotfix/*`: 热修复分支

## API开发

### 1. 路由定义

在 `backend/app/api/v1/endpoints/` 目录下创建新的端点文件：

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.example import ExampleCreate, ExampleUpdate, Example
from app.services.example import ExampleService

router = APIRouter()

@router.get("/", response_model=list[Example])
async def get_examples(
    db: AsyncSession = Depends(get_db)
):
    """获取示例列表"""
    service = ExampleService(db)
    return await service.get_all()

@router.post("/", response_model=Example)
async def create_example(
    example: ExampleCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建示例"""
    service = ExampleService(db)
    return await service.create(example)
```

### 2. 数据模型

在 `backend/app/models/` 目录下定义SQLAlchemy模型：

```python
from datetime import datetime
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class Example(Base):
    __tablename__ = "examples"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

### 3. Pydantic模型

在 `backend/app/schemas/` 目录下定义Pydantic模型：

```python
from datetime import datetime
from pydantic import BaseModel

class ExampleBase(BaseModel):
    name: str

class ExampleCreate(ExampleBase):
    pass

class ExampleUpdate(ExampleBase):
    pass

class Example(ExampleBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

## 前端开发

### 1. 组件开发

使用Vue 3 Composition API：

```vue
<template>
  <div class="example-component">
    <h2>{{ title }}</h2>
    <el-button @click="handleClick">点击</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  title: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  click: [value: string]
}>()

const handleClick = () => {
  emit('click', 'clicked')
}
</script>

<style scoped>
.example-component {
  padding: 20px;
}
</style>
```

### 2. 状态管理

使用Pinia进行状态管理：

```typescript
// stores/example.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useExampleStore = defineStore('example', () => {
  const items = ref([])
  const loading = ref(false)

  const fetchItems = async () => {
    loading.value = true
    try {
      const response = await fetch('/api/items')
      items.value = await response.json()
    } finally {
      loading.value = false
    }
  }

  return {
    items,
    loading,
    fetchItems
  }
})
```

### 3. API调用

创建API服务：

```typescript
// utils/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      // 处理未授权
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

## 爬虫开发

### 1. 爬虫任务

在 `backend/app/tasks/` 目录下创建Celery任务：

```python
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "silence_spider",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

@celery_app.task
def crawl_wechat_account(biz: str):
    """爬取微信公众号"""
    # 实现爬虫逻辑
    pass
```

### 2. 浏览器自动化

使用Playwright进行浏览器自动化：

```python
from playwright.async_api import async_playwright

async def crawl_with_playwright():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # 设置代理
        if settings.PROXY_ENABLED:
            await page.route("**/*", lambda route: route.continue_(
                proxy=settings.PROXY_URL
            ))
        
        # 访问页面
        await page.goto("https://mp.weixin.qq.com/")
        
        # 执行爬虫逻辑
        # ...
        
        await browser.close()
```

## 测试

### 1. 后端测试

使用pytest进行测试：

```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_examples():
    response = client.get("/api/v1/examples/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### 2. 前端测试

使用Vitest进行测试：

```typescript
// tests/components/ExampleComponent.test.ts
import { mount } from '@vue/test-utils'
import ExampleComponent from '@/components/ExampleComponent.vue'

describe('ExampleComponent', () => {
  it('renders correctly', () => {
    const wrapper = mount(ExampleComponent, {
      props: { title: 'Test Title' }
    })
    expect(wrapper.text()).toContain('Test Title')
  })
})
```

## 部署

### 1. 生产环境部署

使用Docker Compose进行部署：

```bash
# 构建并启动生产环境
docker-compose -f docker-compose.prod.yml up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 2. 环境变量配置

创建 `.env` 文件配置环境变量：

```env
# 数据库配置
DATABASE_URL=postgresql+asyncpg://user:password@localhost/silence_spider
REDIS_URL=redis://localhost:6379/0

# 安全配置
SECRET_KEY=your-secret-key-here
DEBUG=false

# 爬虫配置
CRAWLER_DELAY=1.0
CRAWLER_TIMEOUT=30
PROXY_ENABLED=false
```

## 监控和日志

### 1. 日志配置

使用loguru进行日志管理：

```python
from loguru import logger

# 配置日志
logger.add(
    "logs/app.log",
    rotation="1 day",
    retention="30 days",
    level="INFO"
)
```

### 2. 性能监控

使用Prometheus进行性能监控：

```python
from prometheus_client import Counter, Histogram

# 定义指标
request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
```

## 常见问题

### 1. 数据库连接问题

确保PostgreSQL服务正在运行，并且连接字符串正确。

### 2. Redis连接问题

确保Redis服务正在运行，并且端口配置正确。

### 3. 前端构建问题

确保Node.js版本正确，并且所有依赖都已安装。

### 4. Docker构建问题

确保Docker和Docker Compose版本兼容，并且有足够的磁盘空间。

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。 