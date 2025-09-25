#!/bin/bash

echo "=== NestEgg 本地测试脚本 ==="
echo ""

# 检查 uv 是否安装
if ! command -v uv &> /dev/null; then
    echo "正在安装 uv..."
    pip install uv
fi

# 后端设置
echo "1. 设置后端环境..."
cd backend

# 创建虚拟环境
if [ ! -d ".venv" ]; then
    uv venv
fi

# 激活虚拟环境并安装依赖
source .venv/bin/activate
echo "安装后端依赖..."
uv pip install fastapi uvicorn sqlmodel "python-jose[cryptography]" python-multipart pydantic-settings

# 创建 .env 文件
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "已创建 .env 文件"
fi

# 启动后端
echo "启动后端服务..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "后端 PID: $BACKEND_PID"

# 等待后端启动
sleep 5

# 前端设置
echo ""
echo "2. 设置前端环境..."
cd ../frontend

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

# 启动前端
echo "启动前端服务..."
npm run dev &
FRONTEND_PID=$!
echo "前端 PID: $FRONTEND_PID"

echo ""
echo "=== 服务已启动 ==="
echo "后端: http://localhost:8000"
echo "前端: http://localhost:5173"
echo "API 文档: http://localhost:8000/docs"
echo ""
echo "管理员密码: admin123"
echo "普通用户密码: user123"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待中断信号
trap "echo '停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM
wait