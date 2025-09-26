# NestEgg 项目开发文档

## 重要信息

### Git 仓库
- **远程仓库**: https://github.com/sunxth/NestEgg.git
- **⚠️ 重要警告**: 绝对不要自动推送代码到远程仓库！
- **推送规则**: 只有当用户明确主动要求"提交代码变更到远端repo"、"推送到远程"、"同步远端"等类似表述时，才可以执行 `git push`
- **默认行为**: 只进行本地提交 (`git commit`)，不推送到远程

### 项目结构
```
NestEgg/
├── backend/        # FastAPI后端
├── frontend/       # Vue 3前端
├── deploy/         # 部署配置
└── docs/          # 文档
```

### 技术栈
- **后端**: FastAPI + SQLModel + SQLite
- **前端**: Vue 3 + Vite + Tailwind CSS + Chart.js
- **认证**: JWT Token（管理员/普通用户）

### 默认账号
- 管理员密码: admin123
- 普通用户密码: user123

### 核心功能
1. 资金池管理（初始资金: 47,830）
2. 收支记录（income/expense）
3. 多视图展示（首页、记账、收支、日历、统计、设置）
4. 数据可视化（Chart.js图表）

### 开发环境启动
```bash
# 后端
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload

# 前端
cd frontend
npm run dev
```

### API端点
- 认证: `/api/auth/login`
- 交易: `/api/transactions/`
- 资金池: `/api/fund-pool/`
- 统计: `/api/transactions/stats/`
- 导出: `/api/export/`

### 已移除功能
- ~~月度预算功能~~ (已删除，保持应用简洁)
- ~~资产管理功能~~ (已删除，专注记账功能)

### 待实现功能
- [ ] 账单提醒
- [ ] 数据导入功能
- [ ] 多用户支持