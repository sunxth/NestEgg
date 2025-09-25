# NestEgg 项目开发文档

## 重要信息

### Git 仓库
- **远程仓库**: https://github.com/sunxth/NestEgg.git
- **注意**: 不要自动推送代码到远程仓库，除非用户明确要求

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
3. 多视图展示（首页、收支、日历、统计、资产）
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

### 待实现功能
- [ ] 预算管理功能
- [ ] 账单提醒
- [ ] 数据导入功能
- [ ] 多用户支持