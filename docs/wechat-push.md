# 微信推送配置指南

NestEgg 支持通过 Server酱 自动推送周报/月报到微信。

## 快速开始

### 步骤1：获取 Server酱 SendKey

1. 访问 [Server酱官网](https://sct.ftqq.com/)
2. 使用 GitHub 账号登录
3. 微信扫码绑定（你和家人都需要各自绑定）
4. 复制你的 SendKey（格式：`SCT123456xxxxx`）

### 步骤2：配置后端

编辑 `backend/.env` 文件，添加以下配置：

```bash
# Server酱推送配置（多个接收者用逗号分隔）
SERVERCHAN_KEYS=SCT123xxx,SCT456xxx

# 启用周报（每周一发送）
ENABLE_WEEKLY_REPORT=true
WEEKLY_REPORT_TIME=09:00

# 启用月报（每月1号发送）
ENABLE_MONTHLY_REPORT=true
MONTHLY_REPORT_TIME=09:00
```

### 步骤3：重启后端服务

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

启动后会看到类似提示：
```
✅ 已启用周报推送：每周一 09:00
✅ 已启用月报推送：每月1号 09:00
📅 定时任务调度器已启动
```

## 测试推送

### 方法1：通过 API 测试（推荐）

使用管理员账号登录后，调用测试 API：

```bash
# 测试周报推送
curl -X POST "http://localhost:8000/api/reports/test-push" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "send_keys": ["SCT123xxx"],
    "report_type": "weekly"
  }'

# 测试月报推送
curl -X POST "http://localhost:8000/api/reports/test-push" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "send_keys": ["SCT123xxx"],
    "report_type": "monthly"
  }'
```

### 方法2：预览报表内容

```bash
# 预览周报
curl "http://localhost:8000/api/reports/preview/weekly" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 预览月报
curl "http://localhost:8000/api/reports/preview/monthly" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 报表内容示例

### 周报格式

```markdown
## 📊 周报 - 10月01日 - 10月05日

### 💰 收支概览
- **收入**：¥5,000.00
- **支出**：¥2,350.50
- **结余**：🟢 ¥2,649.50
- **交易笔数**：15笔

### 📈 支出分类 TOP5
1. 餐饮：¥850.00
2. 交通：¥320.50
3. 购物：¥680.00
4. 娱乐：¥300.00
5. 其他：¥200.00

---
🤖 NestEgg 自动生成 · 2025-10-05 09:00
```

### 月报格式

```markdown
## 📊 月报 - 2025年10月

### 💰 收支概览
- **收入**：¥20,000.00
- **支出**：¥8,530.50
- **结余**：🟢 ¥11,469.50
- **交易笔数**：52笔
- **日均支出**：¥284.35

### 📈 支出分类 TOP5
1. 餐饮：¥3,200.00
2. 购物：¥2,100.00
3. 交通：¥1,150.50
4. 娱乐：¥980.00
5. 医疗：¥600.00

---
🤖 NestEgg 自动生成 · 2025-10-05 09:00
```

## 可用 API 端点

所有 API 端点需要管理员权限。

### 1. 获取周报数据
```
GET /api/reports/weekly
```

### 2. 获取月报数据
```
GET /api/reports/monthly
```

### 3. 测试推送
```
POST /api/reports/test-push
Body: {
  "send_keys": ["SCT123xxx"],
  "report_type": "weekly"  // 或 "monthly"
}
```

### 4. 预览报表
```
GET /api/reports/preview/weekly   # 周报
GET /api/reports/preview/monthly  # 月报
```

## 配置说明

### SERVERCHAN_KEYS
- 多个 SendKey 用逗号分隔
- 示例：`SCT123xxx,SCT456xxx`
- 支持同时推送给多个家庭成员

### ENABLE_WEEKLY_REPORT
- `true`: 启用周报（每周一发送）
- `false`: 禁用周报

### ENABLE_MONTHLY_REPORT
- `true`: 启用月报（每月1号发送）
- `false`: 禁用月报

### WEEKLY_REPORT_TIME / MONTHLY_REPORT_TIME
- 格式：`HH:MM`（24小时制）
- 示例：`09:00`、`18:30`

## 注意事项

1. **免费额度**：Server酱 免费版每天限制 5 次推送，家庭使用足够
2. **时区**：定时任务使用服务器本地时区
3. **网络要求**：需要服务器能访问 `sctapi.ftqq.com`
4. **多人接收**：每个家庭成员需要各自绑定 Server酱 并获取独立的 SendKey

## 故障排查

### 1. 推送失败
- 检查 SendKey 是否正确
- 确认微信已绑定 Server酱
- 查看后端日志错误信息

### 2. 没有收到推送
- 确认配置中 `ENABLE_WEEKLY_REPORT` 或 `ENABLE_MONTHLY_REPORT` 为 `true`
- 检查推送时间配置
- 使用测试 API 手动触发推送

### 3. 推送内容为空
- 确认数据库中有交易记录
- 检查时间范围内是否有数据
- 使用预览 API 查看报表内容

## 高级用法

### 自定义推送时间（仅周报示例）

如果想在每周五晚上 18:00 发送周报：

1. 修改 `backend/app/services/scheduler.py`：
```python
scheduler.add_job(
    scheduled_weekly_report,
    CronTrigger(day_of_week="fri", hour=18, minute=0),  # 改为周五
    ...
)
```

2. 重启服务

### 添加自定义推送通知

可以在代码中任何位置调用：

```python
from app.services.report import send_to_serverchan

await send_to_serverchan(
    title="🎉 特殊提醒",
    content="今天消费超过预算了！",
    send_key="YOUR_SENDKEY"
)
```

## 未来计划

- [ ] 前端界面配置 Server酱（无需修改 .env）
- [ ] 支持自定义推送模板
- [ ] 添加预算预警推送
- [ ] 支持企业微信群机器人
- [ ] 支持钉钉、飞书推送
