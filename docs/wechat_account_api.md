# 公众号管理 API 使用指南

## 概述

本项目提供了完整的公众号管理 API，支持公众号的增删改查操作。

## API 端点

### 1. 获取公众号列表

**GET** `/api/v1/accounts/`

**参数：**

- `skip` (可选): 跳过记录数，默认 0
- `limit` (可选): 返回记录数，默认 100，最大 1000
- `nickname` (可选): 按公众号名称过滤
- `biz` (可选): 按公众号 biz 过滤
- `is_active` (可选): 按激活状态过滤

**示例：**

```bash
# 获取所有公众号
curl -X GET "http://localhost:8000/api/v1/accounts/"

# 按名称搜索
curl -X GET "http://localhost:8000/api/v1/accounts/?nickname=科技"

# 分页获取
curl -X GET "http://localhost:8000/api/v1/accounts/?skip=0&limit=10"
```

### 2. 获取单个公众号

**GET** `/api/v1/accounts/{account_id}`

**示例：**

```bash
curl -X GET "http://localhost:8000/api/v1/accounts/1"
```

### 3. 根据名称获取公众号

**GET** `/api/v1/accounts/by-nickname/{nickname}`

**示例：**

```bash
curl -X GET "http://localhost:8000/api/v1/accounts/by-nickname/科技日报"
```

### 4. 根据 biz 获取公众号

**GET** `/api/v1/accounts/by-biz/{biz}`

**示例：**

```bash
curl -X GET "http://localhost:8000/api/v1/accounts/by-biz/MjM5NzU2NTY4MQ=="
```

### 5. 创建公众号

**POST** `/api/v1/accounts/`

**请求体：**

```json
{
  "biz": "MjM5NzU2NTY4MQ==",
  "nickname": "科技日报",
  "account": "kejiribao",
  "description": "科技新闻资讯",
  "avatar": "https://example.com/avatar.jpg",
  "qrcode": "https://example.com/qr.jpg",
  "is_verified": true,
  "is_active": true
}
```

**示例：**

```bash
curl -X POST "http://localhost:8000/api/v1/accounts/" \
  -H "Content-Type: application/json" \
  -d '{
    "biz": "MjM5NzU2NTY4MQ==",
    "nickname": "科技日报",
    "description": "科技新闻资讯"
  }'
```

### 6. 更新公众号

**PUT** `/api/v1/accounts/{account_id}`

**请求体：**

```json
{
  "nickname": "新名称",
  "description": "新描述",
  "is_active": false
}
```

**示例：**

```bash
curl -X PUT "http://localhost:8000/api/v1/accounts/1" \
  -H "Content-Type: application/json" \
  -d '{
    "nickname": "新名称",
    "description": "新描述"
  }'
```

### 7. 删除公众号

**DELETE** `/api/v1/accounts/{account_id}`

**示例：**

```bash
curl -X DELETE "http://localhost:8000/api/v1/accounts/1"
```

### 8. 获取统计信息

**GET** `/api/v1/accounts/stats/overview`

**示例：**

```bash
curl -X GET "http://localhost:8000/api/v1/accounts/stats/overview"
```

## 数据模型

### WechatAccount 字段说明

| 字段            | 类型     | 说明                   |
| --------------- | -------- | ---------------------- |
| id              | int      | 主键 ID                |
| biz             | str      | 公众号 biz（唯一标识） |
| nickname        | str      | 公众号名称             |
| account         | str      | 公众号账号             |
| description     | str      | 公众号描述             |
| avatar          | str      | 头像 URL               |
| qrcode          | str      | 二维码 URL             |
| article_count   | int      | 文章数量               |
| follower_count  | int      | 粉丝数量               |
| is_verified     | bool     | 是否认证               |
| is_active       | bool     | 是否激活               |
| created_at      | datetime | 创建时间               |
| updated_at      | datetime | 更新时间               |
| last_crawled_at | datetime | 最后爬取时间           |

## 使用场景

### 1. 前端页面集成

```javascript
// 获取公众号列表
async function getAccounts() {
  const response = await fetch("/api/v1/accounts/");
  const data = await response.json();
  return data.accounts;
}

// 创建公众号
async function createAccount(accountData) {
  const response = await fetch("/api/v1/accounts/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(accountData),
  });
  return await response.json();
}
```

### 2. 爬虫集成

```python
# 在爬虫服务中使用
from app.models.wechat_account import WechatAccount
from sqlalchemy.orm import Session

def get_account_by_nickname(db: Session, nickname: str):
    return db.query(WechatAccount).filter(
        WechatAccount.nickname == nickname
    ).first()

def update_account_stats(db: Session, account_id: int, article_count: int):
    account = db.query(WechatAccount).filter(
        WechatAccount.id == account_id
    ).first()
    if account:
        account.article_count = article_count
        account.last_crawled_at = datetime.utcnow()
        db.commit()
```

### 3. 搜索集成

```python
# 在搜索服务中使用
def get_accounts_for_search():
    """获取所有活跃的公众号用于搜索"""
    return db.query(WechatAccount).filter(
        WechatAccount.is_active == True
    ).all()
```

## 注意事项

1. **biz 字段唯一性**: biz 字段是公众号的唯一标识，创建时不能重复
2. **权限控制**: 建议在实际使用时添加用户认证和权限控制
3. **数据验证**: API 会自动验证请求数据的格式和必填字段
4. **错误处理**: 所有 API 都包含完整的错误处理和日志记录
5. **性能优化**: 对于大量数据的查询，建议使用分页和索引优化
