# NestEgg 家庭记账系统

轻量级家庭记账网站，适用于 2核4GB 云服务器部署。

## 技术栈

- **前端**: Vue 3 + Vite + Tailwind CSS + Pinia
- **后端**: FastAPI + SQLModel + SQLite
- **部署**: Nginx + Uvicorn + systemd

## 功能特点

- 区分管理员和普通用户权限
- 管理员可添加/修改/删除记录
- 普通用户仅可查看
- 支持数据导出和备份
- 响应式界面设计

## 快速开始

详见 `docs/deployment.md`