# Silence Spider - 现代化微信爬虫

一个基于最新技术栈的微信公众文章爬虫系统，支持公众号数据采集、分析和检索。

## 技术栈

### 后端
- **FastAPI** - 现代化的Python Web框架，支持异步处理
- **SQLAlchemy 2.0** - 最新的ORM框架，支持异步数据库操作
- **PostgreSQL** - 强大的关系型数据库
- **Redis** - 缓存和任务队列
- **Celery** - 分布式任务队列
- **WebSocket** - 实时通信
- **Pydantic** - 数据验证和序列化
- **Alembic** - 数据库迁移

### 前端
- **Vue 3** - 最新的Vue框架，使用Composition API
- **Vite** - 现代化的构建工具
- **TypeScript** - 类型安全的JavaScript
- **Element Plus** - Vue 3版本的Element UI
- **ECharts 5** - 数据可视化
- **Pinia** - Vue 3状态管理
- **Vue Router 4** - 路由管理

### 爬虫技术
- **Playwright** - 现代化的浏览器自动化
- **aiohttp** - 异步HTTP客户端
- **BeautifulSoup4** - HTML解析
- **代理池管理** - 智能代理切换

## 功能特性

1. **数据采集**
   - 公众号基本信息采集
   - 历史文章列表采集
   - 文章详细内容采集
   - 阅读量、点赞量等数据采集
   - 评论数据采集

2. **数据分析**
   - 数据可视化图表
   - 趋势分析
   - 影响力评估
   - 发文规律分析

3. **数据检索**
   - 全文检索
   - 多维度筛选
   - 高级搜索

4. **系统管理**
   - 任务管理
   - 代理管理
   - 用户管理
   - 系统监控

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

## 快速开始

### 环境要求
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd silence_spider
```

2. **后端设置**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **前端设置**
```bash
cd frontend
npm install
```

4. **数据库设置**
```bash
# 启动PostgreSQL和Redis
# 运行数据库迁移
cd backend
alembic upgrade head
```

5. **启动服务**
```bash
# 后端
cd backend
uvicorn main:app --reload

# 前端
cd frontend
npm run dev
```

## 开发指南

详细的开发指南请参考 [docs/development.md](docs/development.md)

## 许可证

MIT License 