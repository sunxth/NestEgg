"""
定时任务调度器
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.report import send_weekly_report_to_wechat, send_monthly_report_to_wechat
from app.config import get_settings


settings = get_settings()
scheduler = AsyncIOScheduler()


async def scheduled_weekly_report():
    """定时发送周报"""
    if not settings.serverchan_keys:
        print("⚠️ 未配置 Server酱 SendKey，跳过周报发送")
        return

    keys = [k.strip() for k in settings.serverchan_keys.split(",") if k.strip()]
    if keys:
        await send_weekly_report_to_wechat(keys)


async def scheduled_monthly_report():
    """定时发送月报"""
    if not settings.serverchan_keys:
        print("⚠️ 未配置 Server酱 SendKey，跳过月报发送")
        return

    keys = [k.strip() for k in settings.serverchan_keys.split(",") if k.strip()]
    if keys:
        await send_monthly_report_to_wechat(keys)


def start_scheduler():
    """启动定时任务"""
    if settings.enable_weekly_report:
        # 每周一指定时间发送周报
        hour, minute = settings.weekly_report_time.split(":")
        scheduler.add_job(
            scheduled_weekly_report,
            CronTrigger(day_of_week="mon", hour=int(hour), minute=int(minute)),
            id="weekly_report",
            name="每周一发送周报",
            replace_existing=True
        )
        print(f"✅ 已启用周报推送：每周一 {settings.weekly_report_time}")

    if settings.enable_monthly_report:
        # 每月1号指定时间发送月报
        hour, minute = settings.monthly_report_time.split(":")
        scheduler.add_job(
            scheduled_monthly_report,
            CronTrigger(day=1, hour=int(hour), minute=int(minute)),
            id="monthly_report",
            name="每月1号发送月报",
            replace_existing=True
        )
        print(f"✅ 已启用月报推送：每月1号 {settings.monthly_report_time}")

    if settings.enable_weekly_report or settings.enable_monthly_report:
        scheduler.start()
        print("📅 定时任务调度器已启动")
    else:
        print("ℹ️ 未启用任何定时报表推送")


def stop_scheduler():
    """停止定时任务"""
    if scheduler.running:
        scheduler.shutdown()
        print("📅 定时任务调度器已停止")
