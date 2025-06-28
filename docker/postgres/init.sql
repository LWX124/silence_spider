-- 创建数据库扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建微信公众号账户表
CREATE TABLE IF NOT EXISTS wechat_accounts (
    id SERIAL PRIMARY KEY,
    biz VARCHAR(100) UNIQUE NOT NULL,
    nickname VARCHAR(200) NOT NULL,
    account VARCHAR(100),
    description TEXT,
    avatar VARCHAR(500),
    qrcode VARCHAR(500),
    article_count INTEGER DEFAULT 0,
    follower_count INTEGER DEFAULT 0,
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_crawled_at TIMESTAMP
);

-- 创建文章表
CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    author VARCHAR(100),
    digest TEXT,
    content TEXT,
    content_html TEXT,
    url VARCHAR(1000) UNIQUE NOT NULL,
    cover_url VARCHAR(1000),
    biz VARCHAR(100) NOT NULL,
    mid VARCHAR(100) NOT NULL,
    idx INTEGER DEFAULT 0,
    sn VARCHAR(100),
    publish_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_num INTEGER DEFAULT 0,
    like_num INTEGER DEFAULT 0,
    reward_num INTEGER DEFAULT 0,
    comment_num INTEGER DEFAULT 0,
    position INTEGER DEFAULT 0,
    ip_location VARCHAR(100),
    is_original BOOLEAN DEFAULT FALSE,
    is_deleted BOOLEAN DEFAULT FALSE,
    account_id INTEGER REFERENCES wechat_accounts(id)
);

-- 创建任务表
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    task_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    parameters TEXT,
    progress INTEGER DEFAULT 0,
    total_items INTEGER DEFAULT 0,
    processed_items INTEGER DEFAULT 0,
    result TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    user_id INTEGER REFERENCES users(id)
);

-- 创建代理表
CREATE TABLE IF NOT EXISTS proxies (
    id SERIAL PRIMARY KEY,
    host VARCHAR(100) NOT NULL,
    port INTEGER NOT NULL,
    protocol VARCHAR(10) DEFAULT 'http',
    username VARCHAR(100),
    password VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    response_time FLOAT,
    success_rate FLOAT DEFAULT 0.0,
    total_requests INTEGER DEFAULT 0,
    success_requests INTEGER DEFAULT 0,
    country VARCHAR(50),
    region VARCHAR(50),
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP,
    last_verified_at TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_wechat_accounts_biz ON wechat_accounts(biz);
CREATE INDEX IF NOT EXISTS idx_articles_url ON articles(url);
CREATE INDEX IF NOT EXISTS idx_articles_biz ON articles(biz);
CREATE INDEX IF NOT EXISTS idx_articles_mid ON articles(mid);
CREATE INDEX IF NOT EXISTS idx_articles_account_id ON articles(account_id);
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_proxies_host_port ON proxies(host, port);

-- 创建全文搜索索引
CREATE INDEX IF NOT EXISTS idx_articles_title_gin ON articles USING gin(to_tsvector('chinese', title));
CREATE INDEX IF NOT EXISTS idx_articles_content_gin ON articles USING gin(to_tsvector('chinese', content));

-- 插入默认管理员用户
INSERT INTO users (username, email, hashed_password, full_name, is_superuser)
VALUES (
    'admin',
    'admin@silence-spider.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5u.Ge', -- 密码: admin123
    '系统管理员',
    TRUE
) ON CONFLICT (username) DO NOTHING; 