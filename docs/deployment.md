# NestEgg 部署指南

## 系统要求

- **服务器**: 2核 4GB 内存 Linux 服务器（Ubuntu 20.04/22.04 推荐）
- **Python**: 3.10+
- **Node.js**: 18.x
- **域名**: 已解析到服务器 IP

## 项目架构

```
NestEgg/
├── backend/           # FastAPI 后端
│   ├── app/          # 应用代码
│   ├── pyproject.toml # Python 依赖
│   └── .env          # 环境变量
├── frontend/         # Vue 3 前端
│   ├── src/          # 源代码
│   ├── package.json  # Node 依赖
│   └── dist/         # 构建产物
└── deploy/           # 部署配置
    ├── nginx.conf    # Nginx 配置
    ├── nestegg.service # systemd 服务
    └── deploy.sh     # 部署脚本
```

## 手动部署步骤

### 1. 安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python
sudo apt install python3.10 python3.10-venv python3-pip -y

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# 安装 Nginx
sudo apt install nginx -y

# 安装 uv (Python 包管理器)
pip install uv
```

### 2. 部署后端

```bash
# 创建应用目录
sudo mkdir -p /opt/nestegg/backend
cd /opt/nestegg/backend

# 复制后端代码
sudo cp -r /path/to/backend/* .

# 创建虚拟环境
python3.10 -m venv .venv
source .venv/bin/activate

# 安装依赖
uv pip install fastapi uvicorn sqlmodel python-jose python-multipart pydantic-settings

# 创建环境文件
sudo tee .env > /dev/null <<EOF
DATABASE_URL=sqlite:////opt/nestegg/data/nestegg.db
SECRET_KEY=$(openssl rand -hex 32)
ADMIN_PASSWORD=admin123
USER_PASSWORD=user123
ACCESS_TOKEN_EXPIRE_MINUTES=10080
EOF

# 创建数据目录
sudo mkdir -p /opt/nestegg/data
sudo chown -R www-data:www-data /opt/nestegg
```

### 3. 部署前端

```bash
# 进入前端目录
cd /path/to/frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# 复制到 Web 目录
sudo mkdir -p /var/www/nestegg
sudo cp -r dist/* /var/www/nestegg/
```

### 4. 配置 Nginx

```bash
# 创建 Nginx 配置
sudo tee /etc/nginx/sites-available/nestegg > /dev/null <<'EOF'
server {
    listen 80;
    server_name your-domain.com;

    root /var/www/nestegg;
    index index.html;

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
EOF

# 启用站点
sudo ln -s /etc/nginx/sites-available/nestegg /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 测试并重载 Nginx
sudo nginx -t
sudo systemctl reload nginx
```

### 5. 设置 systemd 服务

```bash
# 创建服务文件
sudo tee /etc/systemd/system/nestegg.service > /dev/null <<'EOF'
[Unit]
Description=NestEgg Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/nestegg/backend
Environment="PATH=/opt/nestegg/backend/.venv/bin"
ExecStart=/opt/nestegg/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable nestegg
sudo systemctl start nestegg

# 查看状态
sudo systemctl status nestegg
```

### 6. 配置 HTTPS (可选)

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo systemctl enable certbot.timer
```

## 本地开发环境

### 启动后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e .
uvicorn app.main:app --reload
```

### 启动前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

## 数据库设计

### Transaction 表

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | INTEGER | 主键 |
| date | DATETIME | 交易日期 |
| amount | DECIMAL(10,2) | 金额 |
| type | VARCHAR | income/expense |
| category | VARCHAR | 分类 |
| description | VARCHAR(200) | 备注 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

## API 接口

### 认证

- `POST /api/auth/login` - 登录

### 交易

- `GET /api/transactions` - 获取交易列表
- `POST /api/transactions` - 创建交易（仅管理员）
- `PUT /api/transactions/{id}` - 更新交易（仅管理员）
- `DELETE /api/transactions/{id}` - 删除交易（仅管理员）

### 统计

- `GET /api/transactions/stats/monthly` - 月度统计
- `GET /api/transactions/stats/category` - 分类统计

### 导出

- `GET /api/export/csv` - 导出 CSV
- `GET /api/export/database` - 备份数据库

## 资源占用预估

- **内存**: ~200MB (FastAPI + Uvicorn + SQLite)
- **CPU**: < 5% (空闲), < 20% (高峰)
- **磁盘**: ~50MB (代码) + 数据增长
- **并发**: 支持 50+ 并发用户

## 安全建议

1. **修改默认密码**: 立即修改 .env 中的默认密码
2. **定期备份**: 使用 cron 定期备份数据库
3. **HTTPS**: 生产环境必须启用 HTTPS
4. **防火墙**: 仅开放必要端口（22, 80, 443）
5. **更新**: 定期更新系统和依赖包

## 备份策略

```bash
# 添加到 crontab
0 2 * * * /opt/nestegg/backup.sh

# 手动备份
cp /opt/nestegg/data/nestegg.db /backup/nestegg_$(date +%Y%m%d).db
```

## 故障排查

```bash
# 查看后端日志
sudo journalctl -u nestegg -f

# 查看 Nginx 日志
sudo tail -f /var/log/nginx/error.log

# 检查端口
sudo netstat -tlnp | grep -E ':(80|443|8000)'

# 重启服务
sudo systemctl restart nestegg
sudo systemctl restart nginx
```

## 性能优化

1. **启用 Gzip**: Nginx 已配置 gzip 压缩
2. **静态缓存**: 可配置静态文件缓存头
3. **数据库索引**: SQLite 自动创建主键索引
4. **CDN**: 可选配置 CDN 加速静态资源

## 升级指南

```bash
# 备份数据
cp /opt/nestegg/data/nestegg.db /backup/

# 更新代码
cd /opt/nestegg/backend
git pull  # 或手动复制新代码

# 更新依赖
source .venv/bin/activate
uv pip install -r pyproject.toml

# 重启服务
sudo systemctl restart nestegg

# 更新前端
cd frontend
npm install
npm run build
sudo cp -r dist/* /var/www/nestegg/
```