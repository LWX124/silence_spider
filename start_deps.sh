#!/bin/bash

echo "🐳 启动 Silence Spider 依赖服务"
echo "================================"

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请先启动Docker"
    exit 1
fi

# 启动依赖服务
echo "🔄 启动 PostgreSQL, Redis, Elasticsearch..."
docker-compose up -d postgres redis elasticsearch

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📋 检查服务状态..."
services=(
    "postgres:5432"
    "redis:6379"
    "elasticsearch:9200"
)

for service in "${services[@]}"; do
    host=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)
    
    if nc -z localhost $port 2>/dev/null; then
        echo "✅ $host 正在运行 (端口 $port)"
    else
        echo "❌ $host 未运行 (端口 $port)"
    fi
done

echo ""
echo "🎉 依赖服务启动完成！"
echo "现在可以运行后端服务了："
echo "  cd backend"
echo "  python debug_local.py"
echo ""
echo "或者手动启动："
echo "  cd backend"
echo "  python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload" 