#!/bin/bash

# NestEgg 部署脚本
# 使用方法: sudo bash deploy.sh

set -e

echo "=== NestEgg 部署脚本 ==="

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then
    echo "请使用 sudo 运行此脚本"
    exit 1
fi

# 变量设置
DOMAIN="your-domain.com"
BACKEND_DIR="/opt/nestegg/backend"
FRONTEND_DIR="/var/www/nestegg"
REPO_URL="https://github.com/yourusername/nestegg.git"

# 1. 安装系统依赖
echo "1. 安装系统依赖..."
apt-get update
apt-get install -y python3.10 python3.10-venv python3-pip nginx certbot python3-certbot-nginx git curl

# 安装 Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# 2. 创建目录
echo "2. 创建应用目录..."
mkdir -p $BACKEND_DIR
mkdir -p $FRONTEND_DIR

# 3. 克隆代码（如果使用 Git）
# echo "3. 克隆代码..."
# git clone $REPO_URL /tmp/nestegg
# cp -r /tmp/nestegg/backend/* $BACKEND_DIR/
# cp -r /tmp/nestegg/frontend/* /tmp/nestegg-frontend/

# 4. 设置后端
echo "4. 设置后端..."
cd $BACKEND_DIR

# 创建虚拟环境
python3.10 -m venv .venv
source .venv/bin/activate

# 安装 uv 和依赖
pip install uv
uv pip install -r pyproject.toml

# 创建 .env 文件
cat > .env <<EOF
DATABASE_URL=sqlite:////opt/nestegg/data/nestegg.db
SECRET_KEY=$(openssl rand -hex 32)
ADMIN_PASSWORD=admin123
USER_PASSWORD=user123
ACCESS_TOKEN_EXPIRE_MINUTES=10080
EOF

# 创建数据目录
mkdir -p /opt/nestegg/data
chown -R www-data:www-data /opt/nestegg

# 5. 构建前端
echo "5. 构建前端..."
cd /tmp/nestegg-frontend
npm install
npm run build
cp -r dist/* $FRONTEND_DIR/

# 6. 配置 Nginx
echo "6. 配置 Nginx..."
cp /path/to/nginx.conf /etc/nginx/sites-available/nestegg
ln -sf /etc/nginx/sites-available/nestegg /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 更新域名
sed -i "s/your-domain.com/$DOMAIN/g" /etc/nginx/sites-available/nestegg

# 7. 配置 SSL
echo "7. 配置 SSL 证书..."
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

# 8. 设置 systemd 服务
echo "8. 配置 systemd 服务..."
cp /path/to/nestegg.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable nestegg
systemctl start nestegg

# 9. 重启 Nginx
echo "9. 重启 Nginx..."
nginx -t
systemctl restart nginx

# 10. 设置防火墙
echo "10. 配置防火墙..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo "=== 部署完成 ==="
echo "访问: https://$DOMAIN"
echo "管理员密码: admin123"
echo "普通用户密码: user123"
echo ""
echo "重要提醒："
echo "1. 请立即修改默认密码"
echo "2. 定期备份 /opt/nestegg/data/nestegg.db"
echo "3. 查看日志: journalctl -u nestegg -f"