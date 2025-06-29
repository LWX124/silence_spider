@echo off
echo 🐳 启动 Silence Spider 依赖服务
echo ================================

REM 检查Docker是否运行
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker未运行，请先启动Docker
    pause
    exit /b 1
)

REM 启动依赖服务
echo 🔄 启动 PostgreSQL, Redis, Elasticsearch...
docker-compose up -d postgres redis elasticsearch

REM 等待服务启动
echo ⏳ 等待服务启动...
timeout /t 10 /nobreak >nul

REM 检查服务状态
echo 📋 检查服务状态...
powershell -Command "Test-NetConnection -ComputerName localhost -Port 5432 -InformationLevel Quiet" >nul 2>&1
if errorlevel 1 (
    echo ❌ postgres 未运行 (端口 5432)
) else (
    echo ✅ postgres 正在运行 (端口 5432)
)

powershell -Command "Test-NetConnection -ComputerName localhost -Port 6379 -InformationLevel Quiet" >nul 2>&1
if errorlevel 1 (
    echo ❌ redis 未运行 (端口 6379)
) else (
    echo ✅ redis 正在运行 (端口 6379)
)

powershell -Command "Test-NetConnection -ComputerName localhost -Port 9200 -InformationLevel Quiet" >nul 2>&1
if errorlevel 1 (
    echo ❌ elasticsearch 未运行 (端口 9200)
) else (
    echo ✅ elasticsearch 正在运行 (端口 9200)
)

echo.
echo 🎉 依赖服务启动完成！
echo 现在可以运行后端服务了：
echo   cd backend
echo   python debug_local.py
echo.
echo 或者手动启动：
echo   cd backend
echo   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause 