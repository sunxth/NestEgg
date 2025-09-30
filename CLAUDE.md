# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NestEgg is a lightweight family accounting system with a FastAPI backend and Vue 3 frontend, designed for 2-core 4GB cloud server deployment. Initial fund pool: 47,830.

## Git Policy

**⚠️ CRITICAL: Absolutely NEVER automatically push or commit to remote repository!**
- Remote: https://github.com/sunxth/NestEgg.git
- **DO NOT run `git commit` or `git push` unless user explicitly requests it**
- User must explicitly say: "提交代码变更到远端repo", "推送到远程", "同步远端", "git commit", "git push", etc.
- Default behavior: **NO git operations** - only make code changes locally
- When user asks to commit/push, confirm what changes will be committed before executing

## Development Commands

### Backend (FastAPI + SQLModel + SQLite)
```bash
cd backend

# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install uv
uv pip install fastapi uvicorn sqlmodel "python-jose[cryptography]" python-multipart pydantic-settings

# Optional dev dependencies
uv pip install pytest httpx ruff

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests (if available)
pytest

# Lint
ruff check .
```

### Frontend (Vue 3 + Vite + Tailwind CSS)
```bash
cd frontend

# Install dependencies
npm install

# Start dev server (runs on http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Quick Start (Both Services)
```bash
./test_local.sh  # Starts both backend (port 8000) and frontend (port 5173)
```

## Architecture

### Backend Structure
```
backend/app/
├── main.py           # FastAPI app, CORS, router registration
├── models.py         # SQLModel schemas: Transaction, FundPool, User roles/enums
├── database.py       # Database initialization and session management
├── auth.py           # JWT authentication, password verification, role checks
├── config.py         # Settings management (loads from .env)
└── routers/
    ├── auth.py       # POST /api/auth/login
    ├── transactions.py  # CRUD + stats endpoints
    ├── fund_pool.py  # GET /api/fund-pool/
    └── export.py     # CSV export, database backup
```

**Key Models:**
- `Transaction`: date, amount, type (income/expense), category, description
- `FundPool`: tracks initial_amount, current_balance, calculates total_deposits/expenses/income
- `UserRole`: ADMIN (can CRUD), USER (read-only)
- `TransactionType`: INCOME, EXPENSE
- `Category`: food, transport, shopping, utilities, entertainment, medical, education, salary, bonus, other

**Authentication:**
- JWT tokens with role-based access control
- Admin password: `admin123` (default)
- User password: `user123` (default)
- Token expiry: 10080 minutes (7 days)
- Admin-only endpoints use `require_admin` dependency

### Frontend Structure
```
frontend/src/
├── App.vue           # Root component with navigation
├── main.js           # Vue app initialization, Pinia, router
├── router/index.js   # Route definitions, auth guards
├── stores/
│   ├── auth.js       # Authentication state (Pinia)
│   └── transaction.js # Transaction data management (Pinia)
├── views/            # Main pages
│   ├── Dashboard.vue    # Fund pool overview, recent transactions
│   ├── Transactions.vue # Transaction list with filters
│   ├── CashFlow.vue     # Income/expense record entry
│   ├── Calendar.vue     # Calendar view of transactions
│   ├── Statistics.vue   # Monthly/category statistics
│   ├── Analytics.vue    # Chart.js visualizations
│   ├── Settings.vue     # User settings, data export
│   └── Login.vue        # Authentication
├── components/       # Reusable UI components
└── utils/           # API client, helpers
```

**State Management (Pinia):**
- `auth` store: Manages login state, user role, JWT token persistence
- `transaction` store: Caches transactions, provides filtering/sorting

**Routing:**
- All routes except `/login` require authentication
- Auth guard redirects unauthenticated users to login
- Logged-in users redirected from `/login` to `/`

### API Endpoints

**Authentication:**
- `POST /api/auth/login` - Login with username/password

**Transactions (read: all users, write: admin only):**
- `GET /api/transactions/` - List transactions (supports date range, type, category filters)
- `POST /api/transactions/` - Create transaction (admin)
- `PUT /api/transactions/{id}` - Update transaction (admin)
- `DELETE /api/transactions/{id}` - Delete transaction (admin)
- `GET /api/transactions/stats/monthly` - Monthly statistics
- `GET /api/transactions/stats/category` - Category breakdown

**Fund Pool:**
- `GET /api/fund-pool/` - Current fund pool status

**Export:**
- `GET /api/export/csv` - Export transactions as CSV
- `GET /api/export/database` - Backup SQLite database

**Health:**
- `GET /api/health` - Service health check

### Database

**SQLite schema:**
- `transaction` table: id, date, amount, type, category, description, created_at, updated_at
- `fundpool` table: id, initial_amount, current_balance, last_updated
- Location: `backend/nestegg.db` (dev) or `/opt/nestegg/data/nestegg.db` (production)

### Configuration

**Backend (.env):**
```
DATABASE_URL=sqlite:///./nestegg.db
SECRET_KEY=<generated>
ADMIN_PASSWORD=admin123
USER_PASSWORD=user123
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

**Frontend:**
- API base URL: `http://localhost:8000` (dev)
- Vite dev server: `http://localhost:5173`
- Production builds served by Nginx with `/api` proxy to backend

## Removed Features

- ~~Monthly budget tracking~~ - Removed to keep app simple
- ~~Asset management~~ - Removed to focus on accounting

## Deployment

Production deployment uses:
- Nginx as reverse proxy (static files + `/api` proxy)
- systemd service for backend (uvicorn)
- Files deployed to `/opt/nestegg/` and `/var/www/nestegg/`
- See `docs/deployment.md` for full deployment guide

## Testing

**Backend:**
- Tests use pytest + httpx (if present)
- Test database created in memory or temp file

**Frontend:**
- No test framework configured yet

## Default Accounts

- Admin: username `admin`, password `admin123`
- User: username `user`, password `user123`

**Security note:** Change default passwords in production via `.env` file.