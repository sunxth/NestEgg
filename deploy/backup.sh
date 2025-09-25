#!/bin/bash

# NestEgg 备份脚本
# 可添加到 crontab 实现定期备份
# 例如: 0 2 * * * /opt/nestegg/backup.sh

BACKUP_DIR="/opt/nestegg/backups"
DB_FILE="/opt/nestegg/data/nestegg.db"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/nestegg_backup_$TIMESTAMP.db"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
cp $DB_FILE $BACKUP_FILE

# 压缩备份文件
gzip $BACKUP_FILE

# 删除 30 天前的备份
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "备份完成: ${BACKUP_FILE}.gz"