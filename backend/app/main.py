from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import init_db
from .routers import auth, transactions, export, fund_pool, reports, settings
from .services.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    start_scheduler()  # 启动定时任务
    yield
    stop_scheduler()  # 停止定时任务


app = FastAPI(
    title="NestEgg API",
    description="Family Accounting System Backend",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(export.router)
app.include_router(fund_pool.router)
app.include_router(reports.router)
app.include_router(settings.router)


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "nestegg-backend"}